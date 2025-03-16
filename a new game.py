import random

# Define the rooms and their descriptions
rooms = {
    "Hall": {
        "description": "You are in a grand hall with a chandelier hanging from the ceiling.",
        "exits": {"north": "Kitchen", "east": "Library"},
        "item": "key"
    },
    "Kitchen": {
        "description": "You are in a kitchen filled with the smell of delicious food.",
        "exits": {"south": "Hall"},
        "item": None
    },
    "Library": {
        "description": "You are in a quiet library filled with books.",
        "exits": {"west": "Hall"},
        "item": "book"
    }
}

# Initialize the player's state
current_room = "Hall"
inventory = []

def show_instructions():
    print("Welcome to the Adventure Game!")
    print("Commands:")
    print("  go [direction] - Move to another room")
    print("  get [item] - Pick up an item")
    print("  inventory - Show your items")
    print("  quit - Exit the game")

def show_status():
    print("\n" + rooms[current_room]["description"])
    if rooms[current_room]["item"]:
        print(f"You see a {rooms[current_room]['item']} here.")
    print("Exits:", ', '.join(rooms[current_room]["exits"].keys()))

def move(direction):
    global current_room
    if direction in rooms[current_room]["exits"]:
        current_room = rooms[current_room]["exits"][direction]
    else:
        print("You can't go that way!")

def get_item(item):
    if rooms[current_room]["item"] == item:
        inventory.append(item)
        rooms[current_room]["item"] = None
        print(f"You picked up the {item}.")
    else:
        print(f"There is no {item} here.")

def show_inventory():
    if inventory:
        print("You have:", ', '.join(inventory))
    else:
        print("Your inventory is empty.")

# Game loop
show_instructions()
while True:
    show_status()
    command = input("> ").lower().strip().split()
    
    if len(command) == 0:
        continue
    
    action = command[0]
    
    if action == "go":
        if len(command) > 1:
            move(command[1])
        else:
            print("Go where?")
    
    elif action == "get":
        if len(command) > 1:
            get_item(command[1])
        else:
            print("Get what?")
    
    elif action == "inventory":
        show_inventory()
    
    elif action == "quit":
        print("Thanks for playing!")
        break
    
    else:
        print("Invalid command.")
