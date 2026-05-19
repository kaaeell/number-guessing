import json
import os
import random
import threading
import time

DIFFICULTIES = {
    "1": {
        "name": "Easy",
        "range": (1, 10),
        "max_guesses": 5,
        "time_limit": 30,
        "points": 100,
    },
    "2": {
        "name": "Medium",
        "range": (1, 50),
        "max_guesses": 8,
        "time_limit": 60,
        "points": 250,
    },
    "3": {
        "name": "Hard",
        "range": (1, 100),
        "max_guesses": 10,
        "time_limit": 90,
        "points": 500,
    },
}

SAVE_FILE = "leaderboard.json"

best_scores = {}
time_up = False
player_name = "Player"
total_points = 0
win_streak = 0
loss_streak = 0

COLD_TAUNTS = [
    "😂 Not even close.",
    "🧊 Ice cold.",
    "😬 Way off.",
    "🌏 Wrong continent.",
    "❄️ Frozen solid.",
]

WARM_CHEERS = [
    "🔥 You're cooking!",
    "😤 SO close.",
    "🎯 Almost there.",
    "👀 Right next to it.",
    "🤏 Tiny difference.",
]

MEDIUM_LINES = [
    "😐 Getting warmer.",
    "🌤 Not bad.",
    "🤔 You're getting there.",
    "💭 Close enough to matter.",
]

LUCKY_LINES = [
    "🍀 FIRST TRY?!",
    "😲 That's insanely lucky.",
    "🎲 What a shot.",
]

WIN_LINES = [
    "🎉 You got it, {name}!",
    "✅ Correct, {name}!",
    "🙌 Nice work, {name}!",
    "🏆 {name} wins.",
]

LOSS_LINES = [
    "💀 Out of guesses, {name}.",
    "😅 Better luck next round, {name}.",
    "🤦 The number was {secret}.",
]

STREAK_WIN_LINES = [
    "🔥 {n} wins in a row!",
    "🚀 {n}-game win streak!",
    "😤 You're unstoppable.",
]

STREAK_LOSS_LINES = [
    "💧 {n} losses in a row.",
    "😬 Rough streak.",
    "🥲 Time for a comeback.",
]

ACHIEVEMENT_LINES = {
    "Speed Demon": "⚡ Achievement unlocked: Speed Demon",
    "Minimalist": "✨ Achievement unlocked: Minimalist",
    "Hintless": "🧠 Achievement unlocked: Hintless Hero",
    "Comeback": "🦅 Achievement unlocked: Comeback",
    "Perfectionist": "💎 Achievement unlocked: Perfectionist",
}


def pick(pool, **kwargs):
    return random.choice(pool).format(**kwargs)


def print_banner():
    print("\n" + "=" * 48)
    print("         🎯 NUMBER GUESSING GAME 🎯")
    print("=" * 48)
    print("      Hints • Streaks • Points • Leaderboard")
    print("=" * 48 + "\n")


def get_player_name():
    global player_name

    name = input("Enter your name: ").strip()

    if name:
        player_name = name

    print(f"\nWelcome, {player_name}!\n")


def choose_difficulty():
    print("Choose a difficulty:\n")

    for key, diff in DIFFICULTIES.items():
        lo, hi = diff["range"]

        print(
            f"[{key}] {diff['name']} "
            f"({lo}-{hi}) | "
            f"{diff['max_guesses']} guesses | "
            f"{diff['time_limit']}s | "
            f"{diff['points']} pts"
        )

    while True:
        choice = input("\nSelect difficulty (1/2/3): ").strip()

        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        print("Invalid choice.")


def load_leaderboard():
    if not os.path.exists(SAVE_FILE):
        return {}

    try:
        with open(SAVE_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, IOError):
        return {}


def save_leaderboard(data):
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file, indent=2)

    except IOError:
        print("Could not save leaderboard.")


def show_all_time_leaderboard():
    data = load_leaderboard()

    if not data:
        print("\n📋 No leaderboard data yet.\n")
        return

    medals = ["🥇", "🥈", "🥉"]

    print("\n" + "─" * 42)
    print("🏅 ALL-TIME LEADERBOARD")
    print("─" * 42)

    for difficulty, entries in data.items():
        print(f"\n{difficulty}:")

        top_scores = sorted(
            entries,
            key=lambda entry: entry["score"],
            reverse=True,
        )[:5]

        for index, entry in enumerate(top_scores):
            medal = medals[index] if index < 3 else f"{index + 1}."

            print(
                f"{medal} "
                f"{entry['name']:12} "
                f"{entry['score']:>5} pts "
                f"({entry['guesses']} guesses)"
            )

    print("\n" + "─" * 42 + "\n")


def update_leaderboard(difficulty_name, score, guesses):
    data = load_leaderboard()

    if difficulty_name not in data:
        data[difficulty_name] = []

    data[difficulty_name].append(
        {
            "name": player_name,
            "score": score,
            "guesses": guesses,
        }
    )

    save_leaderboard(data)


def countdown(time_limit):
    global time_up

    warnings = {time_limit // 2, 10, 5}
    deadline = time.time() + time_limit

    while True:
        remaining = deadline - time.time()

        if remaining <= 0:
            time_up = True
            print(f"\n⏰ Time's up, {player_name}!\n")
            break

        seconds_left = int(remaining)

        if seconds_left in warnings:
            warnings.discard(seconds_left)
            print(f"\n⏳ {seconds_left} seconds remaining.\n")

        time.sleep(0.25)


def warmth_hint(secret, guess, lo, hi):
    difference = abs(secret - guess)
    span = hi - lo

    direction = "higher ↑" if guess < secret else "lower ↓"

    if difference == 0:
        return ""

    if difference <= max(1, span // 10):
        line = pick(WARM_CHEERS)

    elif difference <= max(2, span // 5):
        line = pick(MEDIUM_LINES)

    else:
        line = pick(COLD_TAUNTS)

    return f"Go {direction} | {line}"


def range_hint(secret, guesses, lo, hi):
    current_low = lo
    current_high = hi

    for guess in guesses:
        if guess < secret:
            current_low = max(current_low, guess + 1)

        elif guess > secret:
            current_high = min(current_high, guess - 1)

    print(f"💡 The number is between {current_low} and {current_high}.")


def calculate_points(difficulty, attempts, elapsed, hints_used):
    base_points = difficulty["points"]
    max_guesses = difficulty["max_guesses"]
    time_limit = difficulty["time_limit"]

    efficiency_bonus = (max_guesses - attempts + 1) / max_guesses
    speed_bonus = max(0.5, 1 - (elapsed / time_limit) * 0.5)
    hint_penalty = hints_used * 0.15

    score = int(
        base_points
        * efficiency_bonus
        * speed_bonus
        * (1 - hint_penalty)
    )

    return max(score, 10)


def check_achievements(
    attempts,
    elapsed,
    hints_used,
    max_guesses,
    previous_losses,
):
    achievements = []

    if attempts == 1:
        achievements.append("Minimalist")

    if elapsed < 10:
        achievements.append("Speed Demon")

    if hints_used == 0:
        achievements.append("Hintless")

    if previous_losses >= 3:
        achievements.append("Comeback")

    if max_guesses - attempts >= max_guesses - 1:
        achievements.append("Perfectionist")

    return list(dict.fromkeys(achievements))


def play_round(difficulty):
    global time_up
    global total_points
    global win_streak
    global loss_streak

    time_up = False

    low, high = difficulty["range"]
    max_guesses = difficulty["max_guesses"]
    time_limit = difficulty["time_limit"]

    secret_number = random.randint(low, high)

    guesses = []
    hints_used = 0
    max_hints = 2

    previous_losses = loss_streak

    print("\n" + "─" * 42)
    print(f"Difficulty : {difficulty['name']}")
    print(f"Range      : {low}-{high}")
    print(f"Guesses    : {max_guesses}")
    print(f"Time Limit : {time_limit}s")
    print(f"Hints      : {max_hints}")
    print("Commands   : hint | score | board | quit")
    print("─" * 42 + "\n")

    timer_thread = threading.Thread(
        target=countdown,
        args=(time_limit,),
        daemon=True,
    )

    start_time = time.time()

    timer_thread.start()

    attempt = 0

    while attempt < max_guesses:
        if time_up:
            print(f"The number was {secret_number}.\n")

            loss_streak += 1
            win_streak = 0

            return False, None

        remaining = max_guesses - attempt

        try:
            raw = input(
                f"Guess #{attempt + 1} ({remaining} left): "
            ).strip().lower()

        except EOFError:
            break

        if raw == "hint":
            if hints_used >= max_hints:
                print("No hints remaining.")

            elif remaining <= 1:
                print("Not enough guesses left.")

            else:
                hints_used += 1
                attempt += 1

                range_hint(
                    secret_number,
                    guesses,
                    low,
                    high,
                )

                print(
                    f"Hints used: {hints_used}/{max_hints}"
                )

            continue

        if raw == "score":
            print(
                f"\n📊 Score: {total_points} pts | "
                f"Streak: {win_streak}W/{loss_streak}L\n"
            )

            continue

        if raw == "board":
            show_all_time_leaderboard()
            continue

        if raw in ("quit", "surrender"):
            print(
                f"\n🏳️ You surrendered. "
                f"The number was {secret_number}.\n"
            )

            loss_streak += 1
            win_streak = 0

            return False, None

        try:
            guess = int(raw)

            if not (low <= guess <= high):
                print(f"Enter a number between {low} and {high}.")
                continue

        except ValueError:
            print("Invalid input.")
            continue

        attempt += 1
        guesses.append(guess)

        if guess == secret_number:
            elapsed = time.time() - start_time

            if attempt == 1:
                print(f"\n{pick(LUCKY_LINES)}")

            else:
                print(f"\n{pick(WIN_LINES, name=player_name)}")

            print(
                f"Solved in {attempt} "
                f"guess{'es' if attempt != 1 else ''} "
                f"and {elapsed:.1f}s.\n"
            )

            points = calculate_points(
                difficulty,
                attempt,
                elapsed,
                hints_used,
            )

            total_points += points

            print(
                f"+{points} points | "
                f"Total: {total_points} pts"
            )

            difficulty_name = difficulty["name"]

            previous_best = best_scores.get(difficulty_name)

            if (
                previous_best is None
                or attempt < previous_best
            ):
                best_scores[difficulty_name] = attempt
                print("🏆 New personal best.")

            update_leaderboard(
                difficulty_name,
                points,
                attempt,
            )

            achievements = check_achievements(
                attempt,
                elapsed,
                hints_used,
                max_guesses,
                previous_losses,
            )

            for achievement in achievements:
                print(ACHIEVEMENT_LINES[achievement])

            win_streak += 1
            loss_streak = 0

            if win_streak >= 2:
                print(
                    pick(
                        STREAK_WIN_LINES,
                        n=win_streak,
                        name=player_name,
                    )
                )

            print()

            return True, attempt

        print(
            warmth_hint(
                secret_number,
                guess,
                low,
                high,
            )
        )

        if len(guesses) >= 3:
            print(f"📜 Guess history: {guesses}")

    if not time_up:
        elapsed = time.time() - start_time

        print(
            f"\n{pick(LOSS_LINES, name=player_name, secret=secret_number)}"
        )

        print(f"Time played: {elapsed:.1f}s\n")

    loss_streak += 1
    win_streak = 0

    if loss_streak >= 2:
        print(
            pick(
                STREAK_LOSS_LINES,
                n=loss_streak,
                name=player_name,
            )
        )

    print()

    return False, None


def show_scoreboard(wins, losses):
    print("\n" + "─" * 42)

    print(
        f"Session: {wins}W/{losses}L | "
        f"Points: {total_points} | "
        f"Streak: {win_streak}W"
    )

    if best_scores:
        print("\n📊 Personal Bests:")

        for difficulty, guesses in best_scores.items():
            label = "guess" if guesses == 1 else "guesses"

            print(f"{difficulty:6} → {guesses} {label}")

    print("─" * 42 + "\n")


def main():
    print_banner()

    get_player_name()

    show_all_time_leaderboard()

    wins = 0
    losses = 0

    while True:
        difficulty = choose_difficulty()

        won, _ = play_round(difficulty)

        if won:
            wins += 1

        else:
            losses += 1

        show_scoreboard(wins, losses)

        again = input("Play again? (y/n): ").strip().lower()

        if again not in ("y", "yes"):
            print(
                f"\nThanks for playing, {player_name}!"
            )

            print(f"Final score: {total_points} pts 👋\n")

            show_all_time_leaderboard()

            break


if __name__ == "__main__":
    main()
