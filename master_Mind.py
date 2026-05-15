#!/bin/python3
# MasterMind
# by ICTROCN
# v1.01
# 15-8-2024
# Last mod by DevJan : added loop for replay
import random

print("MasterMind")

COLORS = {
    "R": "Rood",
    "G": "Groen",
    "B": "Blauw",
    "Y": "Geel",
    "O": "Oranje",
    "P": "Paars",
}


def generate_Code(length=4):
    return [random.choice(list(COLORS.keys())) for _ in range(length)]


def parse_Guess(raw_guess):
    cleaned_guess = raw_guess.strip().upper()

    if len(cleaned_guess) == 4 and all(c in COLORS for c in cleaned_guess):
        return list(cleaned_guess)

    color_names = {name.upper(): code for code, name in COLORS.items()}
    parts = cleaned_guess.replace(",", " ").split()
    if len(parts) != 4:
        return None

    guess = []
    for part in parts:
        if part in COLORS:
            guess.append(part)
        elif part in color_names:
            guess.append(color_names[part])
        else:
            return None

    return guess

def get_Feedback(secret, guess):
    black_Pegs = sum(s == g for s, g in zip(secret, guess))
    
    # Count whites by subtracting black and calculating min digit frequency match
    secret_Counts = {}
    guess_Counts = {}

    for s, g in zip(secret, guess):
        if s != g:
            secret_Counts[s] = secret_Counts.get(s, 0) + 1
            guess_Counts[g] = guess_Counts.get(g, 0) + 1

    white_Pegs = sum(min(secret_Counts.get(d, 0), guess_Counts.get(d, 0)) for d in guess_Counts)
    
    return black_Pegs, white_Pegs

def show_Secret(mystery):
    print(mystery)

def play_Mastermind():
    print("Welcome to Mastermind!")
    print("Guess the 4-digit code. Each digit is from 1 to 6. You have 10 attempts.")
    secret_Code = generate_Code()
    attempts = 10

    for attempt in range(1, attempts + 1):
        guess = ""
        valid_Guess = False
        while not valid_Guess:
            raw_Guess = input(f"Attempt {attempt}: ")
            guess = parse_Guess(raw_Guess)
            valid_Guess = guess is not None
            if not valid_Guess:
                print("Invalid input. Enter 4 digits, each from 1 to 6.")
            show_Secret(secret_Code) if raw_Guess == "cheat" else False

        black, white = get_Feedback(secret_Code, guess)
        print(f"Black pegs (correct position): {black}, White pegs (wrong position): {white}")

        if black == 4:
            print(f"Congratulations! You guessed the code: {''.join(secret_Code)}")
            return

    print(f"Sorry, you've used all attempts. The correct code was: {''.join(secret_Code)}")

if __name__ == "__main__":
    again = 'Y'
    while again == 'Y' :
        play_Mastermind()
        again  = input (f"Play again (Y/N) ?").upper()

