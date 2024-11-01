# QuizBot 🔢
This is a bot I was commissioned to make.
Its purpose is to send a message with a quiz, which rewards you a role if you succeed.

## Usage 🤼 
It has a `!start` command which sends a persistent message with an embed and a start button.
If you press the start button, it will send a random quiz question with 4 randomized answers.
If you get any of the questions wrong, you must start from scratch.
If you get all of them right, you get a role which can be changed in the `extensions/quiz/main.py` file.
