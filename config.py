from helpers.dataclasses import Question


BOT_TOKEN: str = (
    "cool"
)
EXTENSIONS: list[str] = ["extensions.quiz"]

ENGLISH_ROLE_ID: int = 00000000000000
MATH_ROLE_ID: int = 00000000000000

ENGLISH_QUESTION_1: Question = Question.with_answers(
    "What is adding two numbers together called?",
    answers=["Addition", "Subtraction", "Multiplication", "Division"],
    correct="Addition",
)

ENGLISH_QUESTION_2: Question = Question.with_answers(
    "What is deducting two numbers together called?",
    answers=["Addition", "Subtraction", "Multiplication", "Division"],
    correct="Subtraction",
)

ENGLISH_QUESTION_3: Question = Question.with_answers(
    "What is enlarging two numbers together called (not adding)?",
    answers=["Addition", "Subtraction", "Multiplication", "Division"],
    correct="Multiplication",
)

ENGLISH_QUESTIONS: list[Question] = [
    ENGLISH_QUESTION_1,
    ENGLISH_QUESTION_2,
    ENGLISH_QUESTION_3,
]


MATH_QUESTION_1: Question = Question.with_answers(
    "What is 1+1?", answers=["2", "3", "4", "5"], correct="2"
)

MATH_QUESTION_2: Question = Question.with_answers(
    "What is 1+2?", answers=["2", "3", "4", "5"], correct="3"
)

MATH_QUESTION_3: Question = Question.with_answers(
    "What is 1+3?", answers=["2", "3", "4", "5"], correct="4"
)

MATH_QUESTIONS: list[Question] = [MATH_QUESTION_1, MATH_QUESTION_2, MATH_QUESTION_3]
