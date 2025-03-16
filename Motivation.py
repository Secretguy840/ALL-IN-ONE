def get_motivation():
    # List of motivational sentences
    motivations = [
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
        "Your time is limited, don't waste it living someone else's life. – Steve Jobs",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt"
    ]
    
    # Display 5 motivational sentences
    for i, sentence in enumerate(motivations, 1):
        print(f"{i}. {sentence}")

def main():
    # Ask the user if they want motivation
    response = input("Do you need some motivation today? (yes/no): ").strip().lower()
    
    if response == "yes":
        print("\nHere are 5 motivational sentences to inspire you:\n")
        get_motivation()
    elif response == "no":
        print("\nThanks for visiting! Have a great day!")
    else:
        print("\nInvalid input. Please type 'yes' or 'no'.")

# Run the program
if __name__ == "__main__":
    main()
