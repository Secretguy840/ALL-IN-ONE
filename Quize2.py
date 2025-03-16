# World Quiz Game with Feedback

def quiz():
    questions = {
        "What is the capital of Australia?": "A) Sydney\nB) Canberra\nC) Melbourne\nD) Brisbane",
        "Which country has the longest coastline?": "A) Canada\nB) Russia\nC) Australia\nD) USA",
        "What is the smallest country in the world?": "A) Monaco\nB) Vatican City\nC) Nauru\nD) San Marino"
    }

    answers = {
        "What is the capital of Australia?": "B",
        "Which country has the longest coastline?": "A",
        "What is the smallest country in the world?": "B"
    }

    score = 0

    for question in questions:
        print(question)
        print(questions[question])
        answer = input("Your answer: ").strip().upper()
        if answer == answers[question]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer is {answers[question]}.\n")

    print(f"Your final score is {score}/{len(questions)}.")
    if score == len(questions):
        print("Excellent! You got all the answers right!")
    elif score > len(questions) / 2:
        print("Good job! You have a decent knowledge of world geography.")
    else:
        print("Keep trying! You can improve your knowledge.")

if __name__ == "__main__":
    quiz()
