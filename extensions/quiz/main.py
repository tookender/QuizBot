import random
from copy import copy

import discord
from discord import Embed, Message
from discord.ext import commands
from helpers.dataclasses import Answer, Question
import config


class Button(discord.ui.Button["Questionnaire"]):
    def __init__(self, answer: Answer) -> None:
        self.answer: Answer = answer
        super().__init__(style=discord.ButtonStyle.blurple, label=str(answer.index))
        # If you want A, B, C, ...: chr(answer.index + 64)
        # If you want 1, 2, 3, ...: str(answer.index)

    async def callback(self, interaction: discord.Interaction) -> None:
        if not self.view:
            return

        if self.answer.is_correct:
            return await self.view.next(interaction)

        embed: Embed = Embed(
            title="❌ You failed!",
            description="Better luck next time...",
            color=discord.Color.red(),
        )

        await interaction.response.edit_message(embed=embed, view=None)


class Questionnaire(discord.ui.View):
    def __init__(
        self, owner: discord.abc.User, role: discord.Role, questions: list[Question]
    ) -> None:
        super().__init__()
        self.owner: discord.abc.User = owner
        self.role: discord.Role = role
        qst: list[Question] = copy(questions)
        random.shuffle(qst)
        self.questions: list[Question] = qst

    def make_embed(self, question: Question) -> Embed:
        embed: Embed = Embed(title=question.question)
        ret: list[str] = [f"**{a.index})** {a.text}" for a in question.answers]
        # If you want A, B, C, ...: {chr(a.index + 64)}
        # If you want 1, 2, 3, ...: {a.index}
        embed.description = "\n".join(ret)
        embed.color = discord.Color.teal()
        return embed

    async def start(self, interaction: discord.Interaction) -> None:
        try:
            next_question: Question = self.questions.pop(0)
            self.clear_items()

            for answer in next_question.answers:
                self.add_item(Button(answer))

            await interaction.response.send_message(
                embed=self.make_embed(next_question), view=self, ephemeral=True
            )

        except IndexError:
            pass

    async def next(self, interaction: discord.Interaction) -> None:
        try:
            next_question: Question = self.questions.pop(0)
            self.clear_items()
            for answer in next_question.answers:
                self.add_item(Button(answer))
            await interaction.response.edit_message(
                embed=self.make_embed(next_question), view=self
            )
        except IndexError:

            embed: Embed = Embed(
                title="🎉 Congratulations",
                description="You finished the quiz!",
                color=discord.Color.green(),
            )

            await interaction.response.edit_message(embed=embed, view=None)
            await interaction.user.add_roles(self.role)  # type: ignore

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.owner == interaction.user


class EnglishStart(discord.ui.View):
    def __init__(self, questions: list[Question]) -> None:
        self.questions: list[Question] = questions
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Start", style=discord.ButtonStyle.green, custom_id="english:start-button"
    )
    async def start(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        view: Questionnaire = Questionnaire(
            owner=interaction.user,
            role=interaction.guild.get_role(config.ENGLISH_ROLE_ID),  # type: ignore
            questions=self.questions,
        )
        await view.start(interaction=interaction)


class MathStart(discord.ui.View):
    def __init__(self, questions: list[Question]) -> None:
        self.questions: list[Question] = questions
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Start", style=discord.ButtonStyle.green, custom_id="math:start-button"
    )
    async def start(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        view: Questionnaire = Questionnaire(
            owner=interaction.user,
            role=interaction.guild.get_role(config.MATH_ROLE_ID),  # type: ignore
            questions=self.questions,
        )
        await view.start(interaction=interaction)


class MainCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    async def cog_load(self) -> None:
        self.bot.add_view(
            EnglishStart(config.ENGLISH_QUESTIONS)
        )  # This makes the English Start button persistent
        self.bot.add_view(
            MathStart(config.MATH_QUESTIONS)
        )  # This makes the Math Start Button persistent

    @commands.group()  # This creates a group command which you can use like this: `!start`
    async def start(self, ctx: commands.Context) -> Message | None:
        if ctx.invoked_subcommand:
            return

        embed: Embed = Embed(
            title="❓ Quiz - Help",
            description="Welcome to the quiz command!\n"
            "This command allows you to start a quiz.\n"
            f"To start the English quiz, use `{ctx.prefix}start english`.\n"
            f"To start the Math quiz, use `{ctx.prefix}start math`.",
            color=discord.Color.teal(),
        )

        embed.set_footer(text="Happy quizzing 🎉")
        return await ctx.send(embed=embed)

    @start.command()  # This creates a subcommand of the start command which you can use like this: `!start english`
    async def english(self, ctx: commands.Context) -> Message:
        embed: Embed = Embed(
            title="❓ English Quiz",
            description="Click on the **`Start`** button below to start the English quiz.\n"
            "To pass, you must answer **ALL** questions correctly.",
            color=discord.Color.yellow(),
        )

        embed.set_footer(text="Good luck 🍀")
        return await ctx.send(
            embed=embed, view=EnglishStart(questions=config.ENGLISH_QUESTIONS)
        )

    @start.command()  # This creates a subcommand of the start command which you can use like this: `!start english`
    async def math(self, ctx: commands.Context) -> Message:
        embed: Embed = Embed(
            title="❓ Math Quiz",
            description="Click on the **`Start`** button below to start the math quiz.\n"
            "To pass, you must answer **ALL** questions correctly.",
            color=discord.Color.blurple(),
        )

        embed.set_footer(text="Good luck 🍀")
        return await ctx.send(
            embed=embed, view=MathStart(questions=config.MATH_QUESTIONS)
        )
