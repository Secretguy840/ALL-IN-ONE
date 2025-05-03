responses = {
    "hi": "Gotta go fast!",
    "eggman": "That no-goodnik won't win!",
    "rings": "Collect 50 to earn a life!",
    "default": "Hmm... not sure what you mean."
}

while True:
    msg = input("You: ").lower()
    print("Sonic:", responses.get(msg, responses["default"]))
