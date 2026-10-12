# Interactive quiz system, sixth version
# Make a dictionary with the questions and correct answers
# Allow the user to choose the option by its label
# Improve the look and usability. Keep track of correct answers.
# Randomize the order of the questions and the order of the answers for each question.
# Refactor the code to use functions.

from string import ascii_lowercase
from pathlib import Path
import random
import json

question_file = Path(__file__).parent / "questions.json"
with open(question_file, "r") as file:
    questions = json.load(file)

hints_file = Path(__file__).parent / "hints.json"
with open(hints_file, "r") as file:
    hints = json.load(file)


NUM_QUESTIONS_PER_QUIZ = 5

def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions.items()), k=num_questions)


def get_answer(question, alternatives, hint):
    labeled_answers = dict(zip(ascii_lowercase, alternatives))

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")

    ask_for_hint(hint)

    while (answer_label := input("Choice? ").lower()) not in labeled_answers:
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")

    return labeled_answers[answer_label]


def ask_for_hint(hint):
    while (choice := input("Would you like a hint? (yes/no) ").lower()) not in ("yes", "no"):
        print("Please enter yes or no.")

    if choice == "yes":
        print(f"Hint: {hint}")


def ask_question(question, alternatives, hint):
    correct_answer = alternatives[0]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))
    answer = get_answer(question, ordered_alternatives, hint)
    if answer == correct_answer:
        print("Correct!")
        return 1
    else:
        print(f"The answer is '{correct_answer!r}', not {answer!r}.")
        return 0


def save_score(score, total_questions):
    score_file = Path(__file__).parent / "score_history.json"

    if score_file.exists():
        with open(score_file, "r") as file:
            score_history = json.load(file)
    else:
        score_history = []

    score_history.append({
        "score": score,
        "total_questions": total_questions
    })

    with open(score_file, "w") as file:
        json.dump(score_history, file, indent=4)


# Main program logic starts here
questions = prepare_questions(questions, NUM_QUESTIONS_PER_QUIZ)

num_correct = 0

# Main Loop
for num, (question, answers) in enumerate(questions, start=1):
    print(f"\nQuestion {num}: {question}")
    num_correct += ask_question(question, answers, hints[question])

print(f"\nYou got {num_correct} correct.")
save_score(num_correct, len(questions))
print("Your score has been recorded.")