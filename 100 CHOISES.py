import random

def introduction():
    print("Welcome to the Ultimate Choice Adventure!")
    print("You will be given choices that lead to different outcomes.")
    print("Try to make the best choices to complete the adventure successfully!")

def make_choice(options):
    print("\nHere are your choices:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a valid number.")

def adventure():
    introduction()
    
    # Starting point
    choices = [
        "Go left", 
        "Go right", 
        "Walk straight", 
        "Climb a tree"
    ]
    
    current_choice = make_choice(choices)
    
    if current_choice == 0:
        print("\nYou go left and find a hidden treasure chest!")
    elif current_choice == 1:
        print("\nYou go right and stumble upon a mysterious forest.")
        choices = ["Enter the forest", "Turn back"]
        current_choice = make_choice(choices)
        if current_choice == 0:
            print("You enter the forest and discover an ancient temple.")
        else:
            print("You turn back and find yourself at a dead end.")
    elif current_choice == 2:
        print("\nYou walk straight and fall into a trap! Game Over.")
    elif current_choice == 3:
        print("\nYou climb a tree and spot a village in the distance.")
        choices = ["Climb down", "Jump to the village"]
        current_choice = make_choice(choices)
        if current_choice == 0:
            print("You climb down and find a peaceful place to rest.")
        else:
            print("You jump but miss and fall into a river! Game Over.")
    
    print("\nWould you like to play again?")
    play_again = input("Enter 'yes' to play again or 'no' to quit: ").strip().lower()
    if play_again == 'yes':
        adventure()
    else:
        print("Thanks for playing! Goodbye.")

if __name__ == "__main__":
    adventure()
