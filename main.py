import asyncio

import discord
from discord.ext import commands

import config


class QuizBot(commands.Bot):
    def __init__(self, initial_extensions: list[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.initial_extensions: list[str] = initial_extensions

    async def setup_hook(self) -> None:
        # Here we are loading all the initial extensions

        for extension in self.initial_extensions:
            await self.load_extension(extension)


async def main() -> None:
    discord.utils.setup_logging()

    async with QuizBot(
        command_prefix=commands.when_mentioned_or("!"),
        intents=discord.Intents.all(),
        initial_extensions=config.EXTENSIONS,
    ) as bot:
        await bot.start(config.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
