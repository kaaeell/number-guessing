import random
import time
import threading

DIFFICULTIES = {
    "1": {"name": "Easy",   "range": (1, 10),  "max_guesses": 5,  "time_limit": 30},
    "2": {"name": "Medium", "range": (1, 50),  "max_guesses": 8,  "time_limit": 60},
    "3": {"name": "Hard",   "range": (1, 100), "max_guesses": 10, "time_limit": 90},
}

best_scores = {}
time_up = False


def print_banner():
    print("\n" + "=" * 42)
    print("        🎯  NUMBER GUESSING GAME  🎯")
    print("=" * 42 + "\n")


def choose_difficulty():
    print("Choose a difficulty:")
    for key, d in DIFFICULTIES.items():
        lo, hi = d["range"]
        print(f"  [{key}] {d['name']:6}  - guess {lo}-{hi}  (up to {d['max_guesses']} tries, {d['time_limit']}s)")
    while True:
        choice = input("\nYour choice (1/2/3): ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Please enter 1, 2, or 3.")


def countdown(time_limit):
    global time_up
    warnings = {time_limit // 2, 10, 5}
    deadline = time.time() + time_limit
    while True:
        remaining = deadline - time.time()
        if remaining <= 0:
            time_up = True
            print("\n\n  ⏰  Time's up!\n")
            break
        left = int(remaining)
        if left in warnings:
            warnings.discard(left)
            print(f"\n  ⏳  {left} seconds left!\n", end="", flush=True)
        time.sleep(0.25)


def warmth_hint(secret, guess, lo, hi):
    diff = abs(secret - guess)
    span = hi - lo

    direction = "higher ↑" if guess < secret else "lower ↓"

    if diff <= max(1, span // 10):
        warmth = "🔥 Scorching hot!"
    elif diff <= max(2, span // 5):
        warmth = "♨️  Very warm!"
    elif diff <= max(3, span // 3):
        warmth = "😐 Getting warmer..."
    else:
        warmth = "🧊 Ice cold."

    return f"  Go {direction}   {warmth}"


def range_hint(secret, guesses_made, lo, hi):
    current_lo, current_hi = lo, hi
    for g in guesses_made:
        if g < secret:
            current_lo = max(current_lo, g + 1)
        elif g > secret:
            current_hi = min(current_hi, g - 1)
    print(f"  💡 Hint: the number is between {current_lo} and {current_hi}.")


def play_round(difficulty):
    global time_up
    time_up = False

    lo, hi = difficulty["range"]
    max_guesses = difficulty["max_guesses"]
    time_limit = difficulty["time_limit"]
    secret = random.randint(lo, hi)
    guesses_made = []
    hints_used = 0
    max_hints = 2

    print(f"\n{'-'*42}")
    print(f"  Difficulty : {difficulty['name']}")
    print(f"  Range      : {lo} - {hi}")
    print(f"  Max tries  : {max_guesses}")
    print(f"  Time limit : {time_limit}s")
    print(f"  Hints      : {max_hints} available  (type 'hint', costs 1 guess)")
    print(f"{'-'*42}\n")
    print("  I've picked a number. Start guessing!\n")

    t = threading.Thread(target=countdown, args=(time_limit,), daemon=True)
    start_time = time.time()
    t.start()

    attempt = 0
    while attempt < max_guesses:
        if time_up:
            print(f"  The number was {secret}.\n")
            return False, None

        remaining_guesses = max_guesses - attempt

        try:
            raw = input(f"  Guess #{attempt + 1} ({remaining_guesses} left): ").strip().lower()
        except EOFError:
            break

        if time_up:
            print(f"  The number was {secret}.\n")
            return False, None

        if raw == "hint":
            if hints_used >= max_hints:
                print("  No hints left!")
            elif remaining_guesses <= 1:
                print("  Not enough guesses to spend on a hint.")
            else:
                hints_used += 1
                attempt += 1
                range_hint(secret, guesses_made, lo, hi)
                print(f"  (Hint {hints_used}/{max_hints} used - {max_guesses - attempt} guesses left)\n")
            continue

        try:
            guess = int(raw)
            if not (lo <= guess <= hi):
                print(f"  Please enter a number between {lo} and {hi}.")
                continue
        except ValueError:
            print("  That's not a valid number. Type a number or 'hint'.")
            continue

        attempt += 1
        guesses_made.append(guess)

        if guess == secret:
            elapsed = time.time() - start_time
            print(f"\n  ✅ Correct! The number was {secret}.")
            print(f"  You got it in {attempt} guess{'es' if attempt != 1 else ''} and {elapsed:.1f} seconds.\n")

            name = difficulty["name"]
            prev = best_scores.get(name)
            if prev is None or attempt < prev:
                best_scores[name] = attempt
                print("  🏆 New personal best!\n")
            return True, attempt

        print(warmth_hint(secret, guess, lo, hi))

        if len(guesses_made) >= 3:
            print(f"  History: {guesses_made}")

    if not time_up:
        print(f"\n  ❌ Out of guesses! The number was {secret}.\n")
    return False, None


def show_scoreboard():
    if not best_scores:
        return
    print("\n  📊 Personal bests this session:")
    for name, score in best_scores.items():
        print(f"      {name:6} -> {score} guess{'es' if score != 1 else ''}")
    print()


def main():
    print_banner()
    wins = losses = 0

    while True:
        difficulty = choose_difficulty()
        won, _ = play_round(difficulty)

        if won:
            wins += 1
        else:
            losses += 1

        show_scoreboard()
        print(f"  Session: {wins}W / {losses}L")

        again = input("\n  Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\n  Thanks for playing! See you next time. 👋\n")
            break


if __name__ == "__main__":
    main()