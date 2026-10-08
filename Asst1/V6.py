from string import ascii_lowercase
import random

questions = {
    "What is the capital of France?": ["Paris", "Toulouse", "Nice", "Avignon"],
    "What is the capital of Germany?": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
    "The last supper was painted by which artist?": ["da Vinci", "Michelangelo", "Raphael", "Caravaggio"]
}

num_questions_per_quiz = 5

num_questions = min(num_questions_per_quiz, len(questions))
selected_questions = random.sample(list(questions.items()), num_questions)

num_correct = 0

for num, (question, answers) in enumerate(selected_questions, start=1):
    correct_answer = answers[0]
    print(f"\nQuestion {num}: {question}")


    sorted_answers = sorted(answers)
    labeled_answers = dict(zip(ascii_lowercase, random.sample(sorted_answers, len(sorted_answers))))

    for label, answer in enumerate(sorted_answers, start=1):
        print(f"{label}. {answer}")

    while(answer_label := input("Choice? ").lower()) not in labeled_answers:
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")

    answer = labeled_answers.get(answer_label)

    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The correct answer is {correct_answer!r}, not {answer!r}.")
