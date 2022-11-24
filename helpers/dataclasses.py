from dataclasses import dataclass
from typing_extensions import Self
import random


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
