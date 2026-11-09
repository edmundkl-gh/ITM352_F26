# Read a file of quiz questions and save as a dictionary
import json

filename = "quiz_questions.json"

with open(filename, "r") as file:
    questions = json.load(file)
    print("Quiz questions loaded:")
    
    for question, options in questions.items():
        print(f"Question: {question}")
        print(f"Options: {options}")
        