import random

print("The computer picks a random number. Try to guess it!")

# random.randint picks a random whole number between 1 and 10
b = random.randint(1, 10)

# Keep looping until the user guesses correctly
while True:
    a = int(input("Type a guess (1-10): "))

    if a < b:
        print("Go up!")
    elif a > b:
        print("Go down!")
    else:
        print("Correct! 🎉")
        break  # stop the loop when the user win 