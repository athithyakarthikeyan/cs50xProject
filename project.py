import random
import time
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme

def instructions():
    """Prints the game instructions using Rich Markdown."""
    game_rules = """
# WORDLY
© 2025 Athithya Karthikeyan. This Python project is protected by copyright law. Unauthorized reproduction or distribution is prohibited.
## HOW TO PLAY

Guess the 5-letter word in 6 tries. The word should be a singular noun.
Letters can be repeated in the word.
The color of the tiles changes after every guess.

## COLOR CODES
- 🟩 Letter is in the correct spot
- 🟨 Letter is in the word but wrong spot
- ⬜ Letter not in the word
---
"""
    console = Console()
    console.print(Markdown(game_rules))

def load_dictionary():
    """Loads the dictionary of 5-letter words."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "five-letter-words.txt")
    try:
        with open(file_path) as file:
            words = [line.strip().lower() for line in file if len(line.strip()) == 5 and line.strip().isalpha()]
            return words
    except FileNotFoundError:
        print("Error: 'five-letter-words.txt' not found. Please make sure it's in the same directory as the script.")
        exit()

def target_word(words):
    """Selects a random target word."""
    return random.choice(words)

def users_guess(valid_words):
    """Prompts the user for a valid guess and checks against local dictionary."""
    while True:
        guess = input("\nYour guess: ").strip().lower()

        if not guess.isalpha():
            print("Your word must contain only letters. Try again!")
            continue

        if len(guess) != 5:
            print("The word must be 5 letters long. Try again!")
            continue

        if guess not in valid_words:
            print("No such word in dictionary. Try again!")
            continue

        return guess

def compare_words(target, guess, letters, i):
    """Compares the guess with the target and assigns colors."""
    target_copy = list(target)
    guess_copy = list(guess)

    # First pass for greens
    for n in range(5):
        if guess[n] == target[n]:
            letters[i][n] = {f" {guess[n]} ": "correct"}
            target_copy[n] = None
            guess_copy[n] = None

    # Second pass for yellows and grays
    for n in range(5):
        if guess_copy[n] is not None:
            if guess_copy[n] in target_copy:
                letters[i][n] = {f" {guess[n]} ": "wrong"}
                target_copy[target_copy.index(guess_copy[n])] = None
            else:
                letters[i][n] = {f" {guess[n]} ": "unable"}

    return letters

def compare_words_emoji(target, guess, emoji, i):
    """Updates emoji board."""
    target_copy = list(target)
    guess_copy = list(guess)

    for n in range(5):
        if guess[n] == target[n]:
            emoji[i][n] = "🟩"
            target_copy[n] = None
            guess_copy[n] = None

    for n in range(5):
        if guess_copy[n] is not None:
            if guess_copy[n] in target_copy:
                emoji[i][n] = "🟨"
                target_copy[target_copy.index(guess_copy[n])] = None

    return emoji

def format_duration(seconds):
    """Formats game time nicely."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    if mins == 0:
        return f"{secs} seconds"
    elif secs == 0:
        return f"{mins} minutes"
    else:
        return f"{mins} minutes {secs} seconds"

def end_screen_victory(target, duration, name):
    msg = f"""
# 🎊 {name.upper()}, YOU GUESSED THE WORD "{target.upper()}" 🎊
⏱️ Time Taken: {format_duration(duration)}
---
"""
    Console().print(Markdown(msg))

def end_screen_loss(target, duration, name):
    msg = f"""
# ❌ {name.upper()}, YOU DIDN'T GUESS THE WORD. IT WAS "{target.upper()}" ❌
⏱️ Time Taken: {format_duration(duration)}
---
"""
    Console().print(Markdown(msg))

def print_board(console, letters):
    """Prints the letter grid."""
    for word in letters:
        for letter in word:
            for key, value in letter.items():
                console.print(key.upper(), style=value, end="")
                console.print(" ", end="")
        print()

def main():
    instructions()
    name = input("ENTER YOUR NAME TO START THE GAME: ").strip() or "Player"
    console = Console()
    console.print(Markdown("\n---\n"))

    valid_words = load_dictionary()
    target = target_word(valid_words)
    # print(f"[debug] target: {target}")  # for testing

    custom_theme = Theme({
        "correct": "bold white on green",
        "wrong": "bold white on yellow",
        "unable": "bold white on #333333",
        "default": "bold white on #111111"
    })
    console_theme = Console(theme=custom_theme)

    letters = [[{"   ": "default"} for _ in range(5)] for _ in range(6)]
    emoji = [["⬜"] * 5 for _ in range(6)]

    start_time = time.time()

    i = 0
    while i < 6:
        print_board(console_theme, letters)
        console.print(Markdown(f"# ROUND {i + 1} of 6"))
        guess = users_guess(valid_words)

        letters = compare_words(target, guess, letters, i)
        emoji = compare_words_emoji(target, guess, emoji, i)

        if guess == target:
            break
        i += 1

    duration = time.time() - start_time

    if guess == target:
        end_screen_victory(target, duration, name)
    else:
        end_screen_loss(target, duration, name)

    print_board(console_theme, letters)
    console.print(Markdown("\n## COPY YOUR EMOJI RESULT"))
    for row in emoji:
        print("".join(row))

    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()
