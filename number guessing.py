import random
import time

# ── Difficulty settings ─────────────────────────────────────────────────────
DIFFICULTIES = {
    "1": {"name": "Easy",   "range": (1, 10),  "max_guesses": 5},
    "2": {"name": "Medium", "range": (1, 50),  "max_guesses": 8},
    "3": {"name": "Hard",   "range": (1, 100), "max_guesses": 10},
}

# ── High-score table (persists for the session) ──────────────────────────────
best_scores = {}   # key: difficulty name → fewest guesses to win


def print_banner():
    print("\n" + "═" * 42)
    print("        🎯  NUMBER GUESSING GAME  🎯")
    print("═" * 42 + "\n")


def choose_difficulty():
    print("Choose a difficulty:")
    for key, d in DIFFICULTIES.items():
        lo, hi = d["range"]
        print(f"  [{key}] {d['name']:6}  — guess 1–{hi}  (up to {d['max_guesses']} tries)")
    while True:
        choice = input("\nYour choice (1/2/3): ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("  Please enter 1, 2, or 3.")


def get_hint(secret, guess, lo, hi):
    """Return a directional hint that narrows the search range."""
    diff = abs(secret - guess)
    span = hi - lo

    if diff == 0:
        return None  # correct — caller handles this

    direction = "higher ↑" if guess < secret else "lower  ↓"

    # Warmth hint
    if diff <= max(1, span // 10):
        warmth = "🔥 Scorching hot!"
    elif diff <= max(2, span // 5):
        warmth = "♨️  Very warm!"
    elif diff <= max(3, span // 3):
        warmth = "😐 Getting warmer…"
    else:
        warmth = "🧊 Ice cold."

    return f"  Go {direction}   {warmth}"


def play_round(difficulty):
    lo, hi = difficulty["range"]
    max_guesses = difficulty["max_guesses"]
    secret = random.randint(lo, hi)
    guesses_made = []
    start_time = time.time()

    print(f"\n{'─'*42}")
    print(f"  Difficulty : {difficulty['name']}")
    print(f"  Range      : {lo} – {hi}")
    print(f"  Max tries  : {max_guesses}")
    print(f"{'─'*42}\n")
    print("  I've picked a number. Start guessing!\n")

    for attempt in range(1, max_guesses + 1):
        remaining = max_guesses - attempt + 1
        prompt = f"  Guess #{attempt} ({remaining} left): "

        # ── get a valid integer input ────────────────────────────────────────
        while True:
            raw = input(prompt).strip()
            try:
                guess = int(raw)
                if lo <= guess <= hi:
                    break
                print(f"  ⚠️  Please enter a number between {lo} and {hi}.")
            except ValueError:
                print("  ⚠️  That's not a number — try again.")

        guesses_made.append(guess)

        if guess == secret:
            elapsed = time.time() - start_time
            print(f"\n  ✅  Correct! The number was {secret}.")
            print(f"  You got it in {attempt} guess{'es' if attempt != 1 else ''}"
                  f" and {elapsed:.1f} seconds.\n")

            # ── update best score ────────────────────────────────────────────
            name = difficulty["name"]
            if name not in best_scores or attempt < best_scores[name]:
                best_scores[name] = attempt
                if name in best_scores:
                    print("  🏆  New personal best for this difficulty!\n")
            return True, attempt

        hint = get_hint(secret, guess, lo, hi)
        print(hint)

        # ── show guess history after the 3rd attempt ─────────────────────────
        if len(guesses_made) >= 3:
            print(f"  History: {guesses_made}")

    # ── out of guesses ───────────────────────────────────────────────────────
    print(f"\n  ❌  Out of guesses! The number was {secret}. Better luck next time!\n")
    return False, None


def show_scoreboard():
    if not best_scores:
        return
    print("\n  📊  Personal bests this session:")
    for diff_name, score in best_scores.items():
        print(f"      {diff_name:6} → {score} guess{'es' if score != 1 else ''}")
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
