import random
import time
import threading
import json
import os

# ── Difficulty presets ────────────────────────────────────────────────────────
DIFFICULTIES = {
    "1": {"name": "Easy",   "range": (1, 10),  "max_guesses": 5,  "time_limit": 30,  "points": 100},
    "2": {"name": "Medium", "range": (1, 50),  "max_guesses": 8,  "time_limit": 60,  "points": 250},
    "3": {"name": "Hard",   "range": (1, 100), "max_guesses": 10, "time_limit": 90,  "points": 500},
}

# save file for the leaderboard, keeping it simple
SAVE_FILE = "leaderboard.json"

# ── Global state ──────────────────────────────────────────────────────────────
best_scores   = {}   # difficulty name → fewest guesses
time_up       = False
player_name   = "friend"
total_points  = 0
win_streak    = 0
loss_streak   = 0

# ── Personality pools ─────────────────────────────────────────────────────────
COLD_TAUNTS = [
    "😂 Not even close. Are you okay?",
    "🧊 Ice cold. Did you just pick randomly?",
    "😬 Yikes. Miles away.",
    "🌏 You're basically on the wrong continent.",
    "❄️  Brrr. Frozen solid.",
]
WARM_CHEERS = [
    "🔥 You're cooking!",
    "😤 SO close — don't choke now.",
    "🎯 You can taste it, can't you?",
    "👀 You're right there. ONE more push.",
    "🤏 Thisclose. Don't overthink it!",
]
MEDIUM_LINES = [
    "😐 Warmer... but not exactly breaking news.",
    "🌤  Getting somewhere. Eventually.",
    "🤔 Middling. Keep going, I believe in you. Kinda.",
    "💭 You're in the neighbourhood. Wrong street though.",
]
LUCKY_LINES = [
    "🍀 Wait — FIRST TRY?! Did you cheat? I'm watching you.",
    "😲 First guess?? Okay statistically that's absurd.",
    "🎲 Lucky shot! Don't let it go to your head.",
]
WIN_LINES = [
    "🎉 Nailed it, {name}!",
    "✅ Got there! Proud of you, {name}.",
    "🙌 YESSS {name}!! You actually did it!",
    "🏆 Boom. {name} wins.",
]
LOSS_LINES = [
    "💀 Out of guesses, {name}. Tough break.",
    "😅 So close… yet so far, {name}.",
    "🤦 The number was RIGHT THERE, {name}.",
    "😮‍💨 That's rough. The number was {secret}. Better luck next time!",
]
STREAK_WIN_LINES = [
    "🔥 {n}-win streak! You're on FIRE, {name}!",
    "🚀 {n} in a row! {name} can't be stopped!",
    "😤 {n} straight wins. Respect.",
]
STREAK_LOSS_LINES = [
    "💧 {n} losses in a row, {name}… it's not your day.",
    "😬 {n}-game skid. The comeback arc starts NOW.",
    "🥲 {n} Ls. Take a breath. You've got this.",
]
ACHIEVEMENT_LINES = {
    "Speed Demon":   "⚡ ACHIEVEMENT: Speed Demon — solved in under 10 seconds!",
    "Minimalist":    "✨ ACHIEVEMENT: Minimalist — won with just 1 guess!",
    "Hintless":      "🧠 ACHIEVEMENT: Hintless Hero — won without using any hints!",
    "Comeback":      "🦅 ACHIEVEMENT: Comeback — won after losing 3+ in a row!",
    "Perfectionist": "💎 ACHIEVEMENT: Perfectionist — solved with max guesses left!",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def pick(pool, **kwargs):
    """Pick a random line from a pool and format it."""
    return random.choice(pool).format(**kwargs)


def print_banner():
    print("\n" + "=" * 44)
    print("       🎯  NUMBER GUESSING GAME  🎯")
    print("=" * 44)
    print("   Hint • Streak • Points • Achievements")
    print("=" * 44 + "\n")


def get_player_name():
    global player_name
    name = input("  What's your name? (press Enter to skip): ").strip()
    player_name = name if name else "Guesser"
    print(f"\n  Alright, {player_name}. Let's see what you've got.\n")


def choose_difficulty():
    print("  Choose a difficulty:")
    for key, d in DIFFICULTIES.items():
        lo, hi = d["range"]
        print(f"    [{key}] {d['name']:6}  — guess {lo}–{hi}  "
              f"({d['max_guesses']} tries, {d['time_limit']}s, {d['points']} pts)")
    while True:
        choice = input("\n  Your choice (1/2/3): ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("  Hmm, just 1, 2, or 3 please.")


# ── Leaderboard (persistent) ──────────────────────────────────────────────────
# i wanted scores to survive after closing the game
# json felt easier than messing with a database lol

def load_leaderboard():
    """Load saved scores from file. Returns empty dict if nothing saved yet."""
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # if the file got corrupted somehow just start fresh
        print("  ⚠️  Couldn't read save file, starting with a clean leaderboard.")
        return {}


def save_leaderboard(leaderboard):
    """Write leaderboard dict to json file."""
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(leaderboard, f, indent=2)
    except IOError:
        # not the end of the world if it fails to save
        print("  ⚠️  Couldn't save leaderboard this time.")


def show_all_time_leaderboard():
    """Print top 5 scores per difficulty from the save file."""
    data = load_leaderboard()
    if not data:
        print("\n  📋 No saved scores yet — be the first!\n")
        return

    medals = ["🥇", "🥈", "🥉"]

    print(f"\n  {'─'*40}")
    print("  🏅 ALL-TIME LEADERBOARD")
    print(f"  {'─'*40}")

    for diff_name, entries in data.items():
        print(f"\n  {diff_name}:")
        sorted_entries = sorted(entries, key=lambda x: x["score"], reverse=True)[:5]
        for i, entry in enumerate(sorted_entries):
            medal  = medals[i] if i < 3 else f"  {i+1}."
            name   = entry.get("name", "???")
            score  = entry.get("score", 0)
            guesses = entry.get("guesses", "?")
            print(f"    {medal} {name:12} {score:>5} pts  ({guesses} guesses)")

    print(f"\n  {'─'*40}\n")


def update_leaderboard(diff_name, score, guesses):
    """Append this round's result and save to file."""
    data = load_leaderboard()

    if diff_name not in data:
        data[diff_name] = []

    data[diff_name].append({
        "name":    player_name,
        "score":   score,
        "guesses": guesses,
    })

    save_leaderboard(data)


# ── Timer thread ──────────────────────────────────────────────────────────────

def countdown(time_limit):
    global time_up
    warnings = {time_limit // 2, 10, 5}
    deadline  = time.time() + time_limit
    while True:
        remaining = deadline - time.time()
        if remaining <= 0:
            time_up = True
            print(f"\n\n  ⏰  Time's up, {player_name}!\n")
            break
        left = int(remaining)
        if left in warnings:
            warnings.discard(left)
            print(f"\n  ⏳  {left} seconds left!\n", end="", flush=True)
        time.sleep(0.25)


# ── Feedback ──────────────────────────────────────────────────────────────────

def warmth_hint(secret, guess, lo, hi):
    diff = abs(secret - guess)
    span = hi - lo
    direction = "higher ↑" if guess < secret else "lower ↓"

    if diff == 0:
        return ""
    elif diff <= max(1, span // 10):
        flavour = pick(WARM_CHEERS)
    elif diff <= max(2, span // 5):
        flavour = pick(MEDIUM_LINES)
    else:
        flavour = pick(COLD_TAUNTS)

    return f"  Go {direction}   {flavour}"


def range_hint(secret, guesses_made, lo, hi):
    cur_lo, cur_hi = lo, hi
    for g in guesses_made:
        if g < secret:
            cur_lo = max(cur_lo, g + 1)
        elif g > secret:
            cur_hi = min(cur_hi, g - 1)
    print(f"  💡 The number is between {cur_lo} and {cur_hi}.")


def calc_points(difficulty, attempts, elapsed, hints_used):
    """Score = base × speed_bonus × efficiency_bonus − hint_penalty."""
    base      = difficulty["points"]
    max_g     = difficulty["max_guesses"]
    time_lim  = difficulty["time_limit"]

    efficiency = (max_g - attempts + 1) / max_g
    speed      = max(0.5, 1 - (elapsed / time_lim) * 0.5)
    hint_pen   = hints_used * 0.15

    score = int(base * efficiency * speed * (1 - hint_pen))
    return max(score, 10)


def check_achievements(attempts, elapsed, hints_used, max_guesses, prior_losses):
    earned = []
    if attempts == 1:
        earned.append("Minimalist")
    if elapsed < 10:
        earned.append("Speed Demon")
    if hints_used == 0:
        earned.append("Hintless")
    if prior_losses >= 3:
        earned.append("Comeback")
    if attempts == 1 and max_guesses > 1:
        pass   # Minimalist already covers this
    if max_guesses - attempts >= max_guesses - 1:
        earned.append("Perfectionist")
    return list(dict.fromkeys(earned))   # deduplicate, keep order


# ── Core round ────────────────────────────────────────────────────────────────

def play_round(difficulty):
    global time_up, total_points, win_streak, loss_streak

    time_up = False
    lo, hi        = difficulty["range"]
    max_guesses   = difficulty["max_guesses"]
    time_limit    = difficulty["time_limit"]
    secret        = random.randint(lo, hi)
    guesses_made  = []
    hints_used    = 0
    max_hints     = 2
    prior_losses  = loss_streak

    print(f"\n  {'─'*40}")
    print(f"  Difficulty : {difficulty['name']}")
    print(f"  Range      : {lo}–{hi}")
    print(f"  Max tries  : {max_guesses}  |  Time: {time_limit}s")
    print(f"  Hints      : {max_hints} available  (type 'hint', costs 1 guess)")
    print(f"  Commands   : 'hint' | 'score' | 'board' | 'quit'")
    print(f"  {'─'*40}\n")
    print(f"  I've picked a number, {player_name}. Let's see what you've got!\n")

    t = threading.Thread(target=countdown, args=(time_limit,), daemon=True)
    start_time = time.time()
    t.start()

    attempt = 0
    while attempt < max_guesses:
        if time_up:
            print(f"  The number was {secret}.\n")
            loss_streak += 1
            win_streak   = 0
            return False, None

        remaining = max_guesses - attempt

        try:
            raw = input(f"  Guess #{attempt + 1}  ({remaining} left): ").strip().lower()
        except EOFError:
            break

        if time_up:
            print(f"  The number was {secret}.\n")
            loss_streak += 1
            win_streak   = 0
            return False, None

        # ── special commands ──────────────────────────────────────────────
        if raw == "hint":
            if hints_used >= max_hints:
                print("  No hints remaining!")
            elif remaining <= 1:
                print("  Not enough guesses to spend on a hint.")
            else:
                hints_used += 1
                attempt    += 1
                range_hint(secret, guesses_made, lo, hi)
                print(f"  (Hint {hints_used}/{max_hints} used — {max_guesses - attempt} guesses left)\n")
            continue

        if raw == "score":
            print(f"\n  📊 Current session score: {total_points} pts  |  "
                  f"Streak: {win_streak}W / {loss_streak}L\n")
            continue

        if raw == "board":
            show_all_time_leaderboard()
            continue

        if raw in ("quit", "surrender"):
            print(f"\n  🏳️  You surrendered. The number was {secret}. Coward. (jk ❤️)\n")
            loss_streak += 1
            win_streak   = 0
            return False, None

        # ── validate number ───────────────────────────────────────────────
        try:
            guess = int(raw)
            if not (lo <= guess <= hi):
                print(f"  Keep it between {lo} and {hi}, yeah?")
                continue
        except ValueError:
            print("  That's not a number. Try again (or type 'hint' / 'quit').")
            continue

        attempt += 1
        guesses_made.append(guess)

        # ── correct! ──────────────────────────────────────────────────────
        if guess == secret:
            elapsed = time.time() - start_time

            if attempt == 1:
                print(f"\n  {pick(LUCKY_LINES)}")
            else:
                print(f"\n  {pick(WIN_LINES, name=player_name)}")

            print(f"  Solved in {attempt} guess{'es' if attempt != 1 else ''} "
                  f"and {elapsed:.1f}s.\n")

            pts = calc_points(difficulty, attempt, elapsed, hints_used)
            total_points += pts
            print(f"  +{pts} points  →  Total: {total_points} pts")

            # update in-session best
            name = difficulty["name"]
            prev = best_scores.get(name)
            if prev is None or attempt < prev:
                best_scores[name] = attempt
                print("  🏆 New personal best!\n")

            # save to leaderboard file
            update_leaderboard(difficulty["name"], pts, attempt)

            achieved = check_achievements(attempt, elapsed, hints_used, max_guesses, prior_losses)
            for a in achieved:
                print(f"  {ACHIEVEMENT_LINES[a]}")
            if achieved:
                print()

            win_streak  += 1
            loss_streak  = 0
            if win_streak >= 2:
                print(f"  {pick(STREAK_WIN_LINES, n=win_streak, name=player_name)}\n")

            return True, attempt

        # ── wrong – give feedback ─────────────────────────────────────────
        print(warmth_hint(secret, guess, lo, hi))

        if len(guesses_made) >= 3:
            print(f"  📜 History: {guesses_made}")

    # ── out of guesses ────────────────────────────────────────────────────────
    if not time_up:
        elapsed = time.time() - start_time
        print(f"\n  {pick(LOSS_LINES, name=player_name, secret=secret)}")
        print(f"  (You took {elapsed:.1f}s)\n")

    loss_streak += 1
    win_streak   = 0
    if loss_streak >= 2:
        print(f"  {pick(STREAK_LOSS_LINES, n=loss_streak, name=player_name)}\n")

    return False, None


# ── Scoreboard ────────────────────────────────────────────────────────────────

def show_scoreboard(wins, losses):
    print(f"\n  {'─'*40}")
    print(f"  Session: {wins}W / {losses}L  |  "
          f"Points: {total_points}  |  "
          f"Streak: {win_streak}W\n")

    if best_scores:
        print("  📊 Personal bests (this session):")
        for diff_name, guesses in best_scores.items():
            print(f"      {diff_name:6} → {guesses} guess{'es' if guesses != 1 else ''}")
    print(f"  {'─'*40}\n")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    print_banner()
    get_player_name()

    # show leaderboard at start so people know what they're competing against
    show_all_time_leaderboard()

    wins = losses = 0

    while True:
        difficulty = choose_difficulty()
        won, _     = play_round(difficulty)

        if won:
            wins   += 1
        else:
            losses += 1

        show_scoreboard(wins, losses)

        again = input("  Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print(f"\n  Thanks for playing, {player_name}! Final score: {total_points} pts 👋\n")
            show_all_time_leaderboard()
            break


if __name__ == "__main__":
    main()