#!/bin/python3
# MasterMind
# by ICTROCN
# v1.01
# 15-8-2024
# Last mod by DevJan : added loop for replay
import random
import sys

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


def format_Code(code):
    return " ".join(COLORS[color] for color in code)

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

def play_Mastermind():
    print("Welkom bij MasterMind!")
    print("Raad de 4-kleurige code.")
    print("Beschikbare kleuren: " + ", ".join(
        f"{code}={name}" for code, name in COLORS.items()
    ))
    print("Je hebt 10 pogingen.")
    secret_Code = generate_Code()
    attempts = 10

    for attempt in range(1, attempts + 1):
        guess = ""
        valid_Guess = False
        while not valid_Guess:
            raw_Guess = input(f"Poging {attempt}: ")
            guess = parse_Guess(raw_Guess)
            valid_Guess = guess is not None
            if not valid_Guess:
                print("Ongeldige invoer. Voer 4 kleuren in, bijvoorbeeld: R G B Y.")

        black, white = get_Feedback(secret_Code, guess)
        print(f"Zwarte pegs (juiste kleur en plek): {black}, "
              f"Witte pegs (juiste kleur, verkeerde plek): {white}")

        if black == 4:
            print(f"Gefeliciteerd! De code was: {format_Code(secret_Code)}")
            return

    print(f"Helaas, je pogingen zijn op. De code was: {format_Code(secret_Code)}")


def run_Tests():
    assert "show_Secret" not in globals()
    assert parse_Guess("cheat") is None
    assert get_Feedback(["R", "G", "B", "Y"], ["R", "G", "B", "Y"]) == (4, 0)
    assert get_Feedback(["R", "G", "B", "Y"], ["Y", "B", "G", "R"]) == (0, 4)
    assert get_Feedback(["R", "R", "G", "B"], ["R", "G", "R", "O"]) == (1, 2)
    print("Tests voor backdoor en get_Feedback geslaagd.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_Tests()
    else:
        again = 'Y'
        while again == 'Y' :
            play_Mastermind()
            again = input("Nog een keer spelen (Y/N)? ").strip().upper()

