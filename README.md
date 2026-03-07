# Number Guessing Game

A small Python game I made for my Introduction to Computing class.

The computer picks a random number between 1 and 10 and you keep guessing until you get it right. It tells you if your guess is too high or too low.

## How to run

```bash
python guessing_game.py
```

## Example

The computer picked a number between 1 and 10.

Type a guess (1-10): 5
Go up!

Type a guess (1-10): 7
Very close!

Type a guess (1-10): 8
Correct! 🎉 You guessed it in 3 tries.

## What I used

- `random.randint` to generate the secret number
- `input()` to get the user's guess
- `while` loop to keep the game going
- `if / elif / else` to check the guess
- `break` to stop the loop when the answer is correct
