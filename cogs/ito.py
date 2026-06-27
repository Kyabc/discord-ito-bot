import json
import random

import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands

from src.model import BaseIto

TOPIC_PATH = "cogs/resources/ito_topic.json"


def load_topic() -> list:
    with open(TOPIC_PATH) as fp:
        topics = json.load(fp)
    return topics


def create_embed(description: str = "") -> discord.Embed:
    embed = discord.Embed(
        title="🂠 ito",
        color=0xB0BFC6,
        description=description
    )
    # embed.set_author(name="GAME: ito")
    return embed


def create_no_game_embed() -> discord.Embed:
    return create_embed(
        "ゲームがありません。\n"
        "`/ito create`で新しいゲームを作成できます。"
    )


class Ito(commands.Cog):
    ito = SlashCommandGroup(name="ito", description="description")

    def __init__(self, bot:commands.bot):
        self.bot = bot
        self.game_state: dict[int, BaseIto] = {}
        self.topics: list[str] = load_topic()

    def check_state(self, channel_id: int) -> bool:
        if channel_id not in self.game_state:
            return False
        return self.game_state[channel_id].state

    @ito.command(name="create", description="Create a new aame")
    async def create(self, ctx: ApplicationContext) -> None:
        channel_id = ctx.channel_id
        if self.check_state(channel_id):
            embed = create_embed(
                "作成済みのゲームがあります。\n"
                "`/ito end`でゲームを終了してください。"
            )
            await ctx.response.send_message(embed=embed)

        self.game_state[channel_id] = BaseIto()
        gstate = self.game_state[channel_id]
        gstate.join(ctx.user.id)
        gstate.state = True
        embed = create_embed(
            f"{ctx.user.display_name}がゲームを作成しました！\n"
            "`/ito join` でゲームに参加できます。"
        )
        embed.add_field(
                name="遊び方",
                value=(
                    "`/ito join` : ゲームに参加\n"
                    "`/ito leave` : ゲームから抜ける\n"
                    "`/ito start` : ゲーム開始\n"
                    "`/ito end` : ゲーム終了"
                ),
                inline=False
            )
        await ctx.response.send_message(embed=embed)

    @ito.command(name="end", description="End the currnet game")
    async def end(self, ctx: ApplicationContext) -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            await ctx.response.send_message(embed=create_no_game_embed())
        else:
            del self.game_state[channel_id]
            embed = create_embed("ゲームを削除しました。")
            await ctx.response.send_message(embed=embed)

    @ito.command(name="join", description="Join the game")
    async def join(self, ctx: ApplicationContext) -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            await ctx.response.send_message(embed=create_no_game_embed())
            return

        gstate = self.game_state[channel_id]
        if not gstate.join(ctx.user.id):
            embed = create_embed(
                "ゲームに参加済みです。\n"
                "`/ito start` でゲームを開始できます。"
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = create_embed(
                f"{ctx.user.display_name}が参加しました！"
            )
            embed.set_thumbnail(url=ctx.user.display_avatar.url)
            embed.add_field(
                    name="現在の参加者",
                    value=self.participants_str(ctx, gstate.players),
                    inline=False
                )
            await ctx.response.send_message(embed=embed)

    @ito.command(name="leave", description="leave the game")
    async def leave(self, ctx: ApplicationContext) -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            await ctx.response.send_message(embed=create_no_game_embed())
            return

        gstate = self.game_state[channel_id]
        if ctx.user.id not in gstate.players:
            embed = create_embed(
                f"{ctx.user.display_name}はゲームに参加していません。\n"
                "`/ito join`でゲームに参加できます。"
            )
            await ctx.response.send_message(embed=embed)
        else:
            gstate.players.remove(ctx.user.id)
            embed = create_embed(f"{ctx.user.display_name}がゲームから退出しました。")
            embed.add_field(
                name="現在の参加者",
                value=self.participants_str(ctx, gstate.players),
                inline=False
            )
            await ctx.response.send_message(embed=embed)


    @ito.command(name="start", description="Start the game and deal cards")
    async def start(self, ctx: ApplicationContext, topic: str = "") -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            embed = create_embed(
                "ゲームがありません。\n"
                "`/ito create`で新しいゲームを作成できます。"
            )
            await ctx.response.send_message(embed=embed)
            return

        gstate = self.game_state[channel_id]
        n = len(gstate.players)
        if n < 2:
            embed = create_embed(
                "ゲームの開始には2人以上の参加が必要です。\n"
                "`/ito join`でゲームに参加できます。"
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return

        if n > 100:
            embed = create_embed(
                "参加人数が100人を超えているためゲームをプレイできません。\n"
                "`/ito leave`でゲームから退出してください。"
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return

        # select topic
        if not topic:
            topic = random.choice(self.topics)
        gstate.state = True
        # deal cards
        numbers = random.sample(range(1, 101), n)
        for user_id, number in zip(gstate.players, numbers, strict=False):
            gstate.cards[user_id] = number
            user = ctx.guild.get_member(user_id)
            await user.send(content=f"🂠 あなたの手札は **{number}** です。\nお題は「{topic}」です。")

        # send topic
        embed = create_embed(
            "ゲームを開始します！\n"
            "DMを確認してください。"
        )
        embed.add_field(name="今回のお題", value=topic)
        await ctx.response.send_message(embed=embed)

    @ito.command(name="open-cards", description="Reveal all players numbers")
    async def open_cards(self, ctx: ApplicationContext) -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            embed = create_embed(
                "ゲームがありません。\n"
                "`/ito create`で新しいゲームを作成できます。"
            )
            await ctx.response.send_message(embed=embed)
            return

        gstate = self.game_state[channel_id]
        lines = []
        for uid, num in sorted(gstate.cards.items(), key=lambda x: x[1]):
            member = ctx.guild.get_member(uid)
            name = member.display_name if member else "Unknown"
            lines.append(f"**{num:>3}** ： {name}")
        embed = create_embed("🎴 カード公開")
        embed.add_field(
            name="結果",
            value="\n".join(lines),
            inline=False
        )
        await ctx.response.send_message(embed=embed)



    @ito.command(name="kick", description="Remove a player from the game")
    async def kick(self, ctx: ApplicationContext, user: discord.User) -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            embed = create_embed(
                "ゲームがありません。\n"
                "`/ito create`で新しいゲームを作成できます。"
            )
            await ctx.response.send_message(embed=embed)
            return

        gstate = self.game_state[channel_id]
        if (not user) or (user.id not in gstate.players):
            embed = create_embed(f"{user.display_name}はゲームに参加していません。")
            await ctx.response.send_message(embed=embed)
            return
        gstate.players.remove(user.id)
        embed = create_embed(f"{user.display_name}をゲームから除外しました。")
        await ctx.response.send_message(embed=embed)

    @ito.command(name="help", description="How to play")
    async def help(self, ctx: ApplicationContext) -> None:
        embed = create_embed("itoの遊び方を表示します。")
        embed.add_field(
            name="コマンド一覧",
            value="**`/ito create`:** ゲームを作成します。\n"
            "**`/ito join`**: ゲームに参加します。\n"
            "**`/ito leave`**: ゲームから退出します。\n"
            "**`/ito start <topic>`**: ゲームを開始します。お題を設定しない場合はランダムに選ばれます。\n"
            "**`/ito open-cards`**: 全員の手札を公開します。\n"
            "**`/ito end`**: ゲームを終了します。\n"
            "**`/ito kick`**: 指定したユーザをキックします。\n"
            "**`/ito state`**: 現在の参加者を表示します。\n",
            inline=False
        )
        await ctx.response.send_message(embed=embed)

    @ito.command(name="state", description="Show the current game state")
    async def state(self, ctx: ApplicationContext) -> None:
        channel_id = ctx.channel_id
        if not self.check_state(channel_id):
            embed = create_embed(
                "ゲームがありません。\n"
                "`/ito create`で新しいゲームを作成できます。"
            )
            await ctx.response.send_message(embed=embed)
            return

        gstate = self.game_state[channel_id]
        embed = create_embed("`/ito join`でゲームに参加できます。")
        embed.add_field(
            name="現在の参加者",
            value=self.participants_str(ctx, gstate.players),
            inline=False
        )
        await ctx.response.send_message(embed=embed)

    def participants_str(self, ctx: ApplicationContext, players: list[int]) -> str:
        names = []
        for uid in players:
            member = ctx.guild.get_member(uid)
            if member:
                names.append(member.display_name)
            else:
                names.append("Unknown")
        return "\n".join(names) if names else "現在の参加者はいません"


def setup(bot: commands.bot):
    bot.add_cog(Ito(bot))
