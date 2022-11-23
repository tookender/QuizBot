import random
from copy import copy
from dataclasses import dataclass

import discord
from discord import Embed, Message, Role
from discord.ext import commands
from typing_extensions import Self


@dataclass
class Answer:
    text: str
    index: int
    is_correct: bool = False

    def __str__(self) -> str:
        return self.text


@dataclass
class Question:
    question: str
    answers: list[Answer]

    @classmethod
    def with_answers(cls, question: str, answers: list[str], correct: str) -> Self:
        if correct not in answers:
            raise RuntimeError("No correct answer.")

        random.shuffle(answers)

        ret: list[Answer] = [
            Answer(text=a, index=idx, is_correct=a == correct)
            for idx, a in enumerate(answers, start=1)
        ]

        return cls(question, ret)


question1: Question = Question.with_answers(
    "What is 1+1?", answers=["2", "3", "4", "5"], correct="2"
)

question2: Question = Question.with_answers(
    "What is 1+2?", answers=["2", "3", "4", "5"], correct="3"
)

question3: Question = Question.with_answers(
    "What is 1+3?", answers=["2", "3", "4", "5"], correct="4"
)

questions: list[Question] = [question1, question2, question3]


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
    def __init__(self, owner: discord.abc.User, questions: list[Question]) -> None:
        super().__init__()
        self.owner: discord.abc.User = owner
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

            role: Role | None = interaction.guild.get_role(0000000000000000000)  # type: ignore
            await interaction.user.add_roles(role)  # type: ignore

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.owner == interaction.user


class Start(discord.ui.View):
    def __init__(self, questions: list[Question]) -> None:
        self.questions: list[Question] = questions
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Start", style=discord.ButtonStyle.green, custom_id="start-button"
    )
    async def start(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        view: Questionnaire = Questionnaire(
            owner=interaction.user,
            questions=self.questions,
        )
        await view.start(interaction=interaction)


class MainCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    async def cog_load(self) -> None:
        self.bot.add_view(Start(questions))

    @commands.command()
    async def start(self, ctx) -> Message:
        embed: Embed = Embed(
            title="❓ Quiz",
            description="Click on the **`Start`** button below to start the quiz.\n"
            "To pass, you must answer **ALL** questions correctly.",
            color=discord.Color.teal(),
        )

        embed.set_footer(text="Good luck 🍀")
        return await ctx.send(embed=embed, view=Start(questions=questions))
