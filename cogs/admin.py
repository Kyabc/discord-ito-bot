import discord
from discord import ApplicationContext, SlashCommandGroup, ui
from discord.ext import commands


class Admin(commands.Cog):
    admin = SlashCommandGroup(name="admin", description="description")

    def __init__(self, bot:commands.bot):
        self.bot = bot

    @admin.command(name="about", description="Shows basic information of this bot.")
    async def about(self, ctx: ApplicationContext) -> None:
        owner_url = "https://discord.com/channels/514366500715364352"
        github_project = "https://github.com/Kyabc/discord-ito-bot"

        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name="ito bot", url=github_project)
        embed.add_field(name="Dev:", value=f"[terry]({owner_url})", inline=True)
        embed.add_field(name="Version:", value=self.bot.bot_version, inline=True)

        view = ui.View()
        view.add_item(ui.Button(label="GitHub", url=github_project, row=0))
        view.add_item(ui.Button(label="KO-FI", url="https://ko-fi.com/terryx_x", row=0))

        await ctx.response.send_message(embed=embed, view=view)


def setup(bot: commands.bot):
    bot.add_cog(Admin(bot))
