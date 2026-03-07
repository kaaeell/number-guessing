import random

print("🎮 Guess the Number Game!")

while True:
    b = random.randint(1, 10)
    attempts = 0

    print("\nThe computer picked a number between 1 and 10.")

    while True:
        a = int(input("Type a guess (1-10): "))
        attempts += 1

        if abs(a - b) == 1:
            print("Very close!")

        if a < b:
            print("Go up!")
        elif a > b:
            print("Go down!")
        else:
            print(f"Correct! 🎉 You guessed it in {attempts} tries.")
            break

    play_again = input("Play again? (yes/no): ").lower()
    if play_again != "yes":
        print("Thanks for playing! 👋")
        break



