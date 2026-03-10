# Number Guessing Game 🎯

A Python terminal game where you guess a randomly picked number.

## How to run

```
python number_guessing.py
```

## Features

- **3 difficulty levels** — Easy (1–10), Medium (1–50), Hard (1–100)
- **Warmth hints** — tells you if you're 🔥 scorching hot or 🧊 ice cold
- **Countdown timer** — you have 30 / 60 / 90 seconds depending on difficulty
- **Hint system** — type `hint` to reveal the narrowed range (costs 1 guess, max 2 per round)
- **Limited tries** — run out of guesses or time and you lose
- **Best score tracker** — keeps your fewest-guess record per difficulty
- **Play again loop** — no need to restart the script

## Example

```
  Guess #1 (5 left): 5
  Go higher ↑   😐 Getting warmer...

  Guess #2 (4 left): hint
  💡 Hint: the number is between 6 and 10.

  Guess #3 (3 left): 8
  ✅ Correct! The number was 8.
  You got it in 3 guesses and 9.4 seconds.
```
