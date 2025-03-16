import random

# Randomized World Quiz Game

def quiz():
    questions = [
        {
            "question": "What is the capital of Italy?",
            "options": ["A) Rome", "B) Paris", "C) Berlin", "D) Madrid"],
            "answer": "A"
        },
        {
            "question": "Which country is known for the Great Wall?",
            "options": ["A) Japan", "B) China", "C) India", "D) Mongolia"],
            "answer": "B"
        },
        {
            "question": "What is the largest desert in the world?",
            "options": ["A) Sahara", "B) Arabian", "C) Gobi", "D) Kalahari"],
            "answer": "A"
        }
    ]

    random.shuffle(questions)  # Shuffle questions

    score = 0

    for q in questions:
        print(q["question"])
        for option in q["options"]:
            print(option)
        answer = input("Your answer: ").strip().upper()
        if answer == q["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer is {q['answer']}.\n")

    print(f"Your final score is {score}/{len(questions)}.")

if __name__ == "__main__":
    quiz()
