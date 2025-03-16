# Basic World Quiz Game

def quiz():
    questions = {
        "What is the capital of France?": "A) Paris\nB) London\nC) Berlin\nD) Madrid",
        "Which country is known as the Land of the Rising Sun?": "A) China\nB) Japan\nC) Thailand\nD) South Korea",
        "What is the largest continent?": "A) Africa\nB) Asia\nC) Europe\nD) Antarctica"
    }

    answers = {
        "What is the capital of France?": "A",
        "Which country is known as the Land of the Rising Sun?": "B",
        "What is the largest continent?": "B"
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

if __name__ == "__main__":
    quiz()
