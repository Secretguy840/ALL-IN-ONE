import random
targets = [random.randint(1, 10) for _ in range(3)]
print("Hit the targets!", targets)
for _ in range(5):
    guess = int(input("Throw ring (1-10): "))
    if guess in targets:
        targets.remove(guess)
        print("Hit!")
print("Score:", 3 - len(targets))
