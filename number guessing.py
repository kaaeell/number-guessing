import random

def get_difficulty():
    print("\nChoose difficulty:")
    print("  1 - Easy   (1–10)")
    print("  2 - Medium (1–50)")
    print("  3 - Hard   (1–100)")
    while True:
        choice = input("Enter 1, 2, or 3: ")
        if choice == "1":
            return 10, "Easy"
        elif choice == "2":
            return 50, "Medium"
        elif choice == "3":
            return 100, "Hard"
        else:
            print("Please enter 1, 2, or 3.")

def get_guess(limit):
    while True:
        try:
            guess = int(input(f"Type a guess (1-{limit}): "))
            if 1 <= guess <= limit:
                return guess
            print(f"Please enter a number between 1 and {limit}.")
        except ValueError:
            print("That's not a valid number. Try again!")

def play_round(limit):
    secret = random.randint(1, limit)
    attempts = 0

    while True:
        guess = get_guess(limit)
        attempts += 1

        if guess == secret:
            print(f"🎉 Correct! You guessed it in {attempts} {'try' if attempts == 1 else 'tries'}.")
            return attempts
        elif abs(guess - secret) <= limit // 10:
            print("🔥 Very close!" + (" Go up!" if guess < secret else " Go down!"))
        elif guess < secret:
            print("⬆️  Go up!")
        else:
            print("⬇️  Go down!")

def main():
    print("🎮 Guess the Number Game!")
    wins = 0
    rounds = 0
    best_score = None

    while True:
        limit, diff_name = get_difficulty()
        print(f"\n[{diff_name}] I picked a number between 1 and {limit}. Good luck!")

        tries = play_round(limit)
        rounds += 1
        wins += 1

        if best_score is None or tries < best_score:
            best_score = tries
            print("🏆 New best score!")

        print(f"📊 Stats — Rounds played: {rounds} | Best score: {best_score} tries")

        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\nThanks for playing! Final best score: {best_score} tries. 👋")
            break

main()