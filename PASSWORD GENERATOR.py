import random
import string

def generate_password(name):
    # Generate a random string of 4 characters
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=4))
    
    # Generate a random number
    random_number = str(random.randint(10, 99))
    
    # Combine the name, random characters, and random number
    password = f"{name}{random_chars}{random_number}"
    
    # Shuffle the password to make it more secure
    password_list = list(password)
    random.shuffle(password_list)
    final_password = ''.join(password_list)
    
    return final_password

def main():
    # Ask for the user's name
    name = input("Please enter your name: ")
    
    # Generate the password
    password = generate_password(name)
    
    # Display the generated password
    print(f"Your generated password is: {password}")

if __name__ == "__main__":
    main()
