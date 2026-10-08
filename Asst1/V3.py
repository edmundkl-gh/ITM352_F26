# Interactive quiz system, second version
# Make a dictionary with the questions and correct answers

questions = {
    "What is the capital of France?": ["Paris", "Toulouse", "Nice", "Avignon"],
    "What is the capital of Germany?": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
    "The last supper was painted by which artist?": ["da Vinci", "Michelangelo", "Raphael", "Caravaggio"]
}

for question, answers in questions.items():
    correct_answer = answers[0]
    answer = input(f"{question} ")
    for answer in answers:
       print(f" - {answer}")

    answer = input(f"{question} ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"Incorrect. The correct answer is {correct_answer}.", not {answer})
    