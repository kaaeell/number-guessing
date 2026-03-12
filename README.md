# Number Guessing Game

A small Python game I made for my Introduction to Computing class. Kept adding stuff to it over time.

The computer picks a random number and you guess until you get it right. It gives you hot/cold feedback, tracks your score, and now saves your results to a leaderboard between sessions.

---

## How to run

```
python "number guessing.py"
```

No extra libraries needed — just Python 3.

---

## Features

- **3 difficulty levels** — Easy (1–10), Medium (1–50), Hard (1–100)
- **Timer** — each round has a time limit, with warnings at half-time, 10s, and 5s
- **Hints** — type `hint` to narrow down the range (costs 1 guess, max 2 per round)
- **Hot/cold feedback** — tells you how close your guess is with personality
- **Score system** — based on difficulty, speed, and how many guesses you used
- **Achievements** — Speed Demon, Minimalist, Hintless Hero, Comeback, Perfectionist
- **Win/loss streaks** — tracks your current streak and talks trash accordingly
- **Persistent leaderboard** — scores are saved to `leaderboard.json` so they survive between sessions

---

## Commands (during a round)

| Command     | What it does                              |
|-------------|-------------------------------------------|
| `hint`      | Narrows the range — costs 1 guess         |
| `score`     | Shows your current session score          |
| `board`     | Shows the all-time leaderboard mid-game   |
| `quit`      | Surrenders the round                      |

---

## Leaderboard

Scores are saved automatically to `leaderboard.json` after every win. The file is created in the same folder as the script. Top 5 per difficulty are shown at the start and end of each session.

Example:
```
  ────────────────────────────────────────
  🏅 ALL-TIME LEADERBOARD
  ────────────────────────────────────────

  Easy:
    🥇 kaaeell       90 pts  (2 guesses)
    🥈 kaaeell       80 pts  (3 guesses)

  Hard:
    🥇 kaaeell      420 pts  (3 guesses)
  ────────────────────────────────────────
```

---

## Scoring

```
score = base_points × efficiency × speed_bonus × (1 − hint_penalty)
```

- **Efficiency**: more guesses left = higher multiplier
- **Speed**: faster = up to 50% bonus
- **Hint penalty**: each hint costs 15% of your score
- Minimum score is 10 (can't go negative)

---

## Achievements

| Achievement      | How to unlock                          |
|------------------|----------------------------------------|
| ✨ Minimalist     | Win on the first guess                 |
| ⚡ Speed Demon    | Solve in under 10 seconds              |
| 🧠 Hintless Hero  | Win without using any hints            |
| 🦅 Comeback       | Win after 3+ consecutive losses        |
| 💎 Perfectionist  | Win with only 1 guess used             |

---

## What I used

- `random.randint` — picks the secret number
- `threading` — runs the countdown timer in the background
- `json` + `os` — saves and loads the leaderboard file
- `time` — measures elapsed time for scoring and the timer
- `while` loops, `if/elif/else`, functions — game logic and structure

---

## What I'd add next

- option to reset/clear the leaderboard
- multiplayer mode where two people take turns
- maybe a GUI version with tkinter someday

---

## About

Made for my Intro to Computing class. Kept updating it whenever I had time.
