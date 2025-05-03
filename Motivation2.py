import random
import time
from pyfiglet import Figlet

def generate_affirmation():
    affirmations = [
        "You are capable of amazing things",
        "Progress, not perfection, is the goal",
        "Your potential is limitless",
        "Challenges make you stronger",
        "You attract positivity and success",
        "Today is full of possibilities",
        "You are enough just as you are",
        "Your dreams are valid and achievable"
    ]
    return random.choice(affirmations)

def display_motivation():
    f = Figlet(font='slant')
    print("\n" + f.renderText('BELIEVE'))
    
    while True:
        print("\n" + "-"*50)
        print(f"\n✨ Your Daily Affirmation: \n\n  {generate_affirmation()} ✨")
        print("\n" + "-"*50)
        
        choice = input("\nAnother one? (y/n): ").lower()
        if choice != 'y':
            print("\n" + f.renderText('YOU GOT THIS!'))
            time.sleep(2)
            break

if __name__ == "__main__":
    display_motivation()
