from extensions.quiz.main import MainCog


class Quiz(MainCog):
    pass


async def setup(bot) -> None:
    await bot.add_cog(Quiz(bot))
