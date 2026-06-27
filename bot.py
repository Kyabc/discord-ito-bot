from __future__ import annotations

import logging

import aiohttp
import discord

from src.settings import settings

logger = logging.getLogger(__name__)

initial_extensions = ["cogs.admin", "cogs.ito"]

intents = discord.Intents.default()
intents.message_content = True


BOT_VERSION = "1.0.0"


class BoardGameBot(discord.Bot):
    bot_app_info: discord.AppInfo

    def __init__(self):
        super().__init__(
            case_insensitive=True,
            intents=intents,
        )
        self.session: aiohttp.ClientSession = None
        self.bot_version = BOT_VERSION

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    async def on_ready(self) -> None:
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name=f"/help | ito bot v{self.bot_version}"
        )
        await self.change_presence(activity=activity)

        try:
            self.owner_id = int(settings.OWNER_ID)
        except ValueError:
            self.bot_app_info = await self.application_info()
            self.owner_id = self.bot_app_info.owner.id

        print(f"ito bot is ready! (ver.{self.bot_version})")
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    def load_cogs(self, extensions) -> None:
        for ext in extensions:
            try:
                self.load_extension(ext, store=False)
                logger.info(f"Loaded extension: {ext}")
            except Exception:
                logger.error(f"Failed to load extension {ext}.", exc_info=True)


def run_bot() -> None:
    bot = BoardGameBot()
    bot.load_cogs(initial_extensions)
    bot.run(settings.DISCORD_TOKEN)
    logger.info("Bot is running.")


if __name__ == "__main__":
    run_bot()
