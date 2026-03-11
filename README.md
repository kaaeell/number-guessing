# 🎯 Number Guessing Game

A terminal number-guessing game with personality — taunts, cheers, streaks, achievements, and a points system.

---

## 🚀 How to run

```bash
python guess_game.py
```

No dependencies. Python 3.7+ only.

---

## 🎮 Gameplay

Pick a difficulty, then guess the secret number before time runs out.

| Difficulty | Range  | Tries | Time | Points |
|------------|--------|-------|------|--------|
| Easy       | 1–10   | 5     | 30s  | 100    |
| Medium     | 1–50   | 8     | 60s  | 250    |
| Hard       | 1–100  | 10    | 90s  | 500    |

---

## ✨ What's new (vs original)

### 👤 Player name
You enter your name at the start and the game addresses you throughout — in wins, losses, streak callouts, and the goodbye message.

### 💬 Personality / humanized messages
Every win, loss, warmth hint, and streak comment is drawn from a randomized pool of snarky or encouraging lines so the game never feels robotic.

### 🏅 Points system
Earn points each round based on:
- **Base value** by difficulty
- **Efficiency bonus** — fewer guesses used → more points
- **Speed bonus** — finish faster → more points
- **Hint penalty** — each hint used deducts 15 % from your multiplier

Your running total is shown after every round and at session end.

### 🔥 Win / loss streaks
The game tracks consecutive wins and losses. Hit 2+ in a row and it calls you out — either hyping you up or gently roasting you.

### 🏆 Achievements
Unlockable badges earned automatically mid-game:

| Badge | Condition |
|-------|-----------|
| ⚡ Speed Demon | Solved in under 10 seconds |
| ✨ Minimalist | Won on the very first guess |
| 🧠 Hintless Hero | Won without using any hints |
| 🦅 Comeback | Won after 3+ consecutive losses |
| 💎 Perfectionist | Won with only 1 guess used |

### 🏳️ Surrender command
Type `quit` or `surrender` at any prompt to give up gracefully. The number is revealed and the round counts as a loss — no judgement (okay, a little).

### 📊 Score command
Type `score` at any point during a round to check your current session points and win/loss record without wasting a guess.

---

## ⌨️ In-round commands

| Input | Action |
|-------|--------|
| A number | Make a guess |
| `hint` | Narrows the range (costs 1 guess, max 2/round) |
| `score` | Shows current points + record (free) |
| `quit` / `surrender` | Gives up and reveals the number |
