#!/bin/python3
# MasterMind
# by ICTROCN
# v1.01
# 15-8-2024
# Last mod by DevJan : added loop for replay
import os
import random

COLORS = {
    "R": "Rood",
    "G": "Groen",
    "B": "Blauw",
    "Y": "Geel",
    "O": "Oranje",
    "P": "Paars",
}

ADMIN_PASSWORD_ENV = "MASTERMIND_ADMIN_PASSWORD"
COLOR_NAMES = {name.upper(): code for code, name in COLORS.items()}


def generate_Code(length=4):
    return [random.choice(list(COLORS.keys())) for _ in range(length)]


def parse_Guess(raw_guess):
    cleaned_guess = raw_guess.strip().upper().replace(",", " ")
    parts = cleaned_guess.split()

    if len(parts) == 1 and len(parts[0]) == 4:
        parts = list(parts[0])

    if len(parts) != 4:
        return None

    guess = []
    for part in parts:
        if part in COLORS:
            guess.append(part)
        elif part in COLOR_NAMES:
            guess.append(COLOR_NAMES[part])
        else:
            return None

    return guess


def format_Code(code):
    return " ".join(COLORS[color] for color in code)


def is_Admin_Password(password):
    admin_Password = os.getenv(ADMIN_PASSWORD_ENV)
    return bool(admin_Password) and password == admin_Password


def load_Admin_Settings(env_File=".env"):
    if os.getenv(ADMIN_PASSWORD_ENV) or not os.path.exists(env_File):
        return

    with open(env_File, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            if key.strip() == ADMIN_PASSWORD_ENV:
                os.environ[ADMIN_PASSWORD_ENV] = value.strip().strip("'\"")
                return


def is_Admin_Command(raw_Guess):
    return raw_Guess.strip().lower() in ("a", "admin")


def admin_Menu(secret_Code):
    load_Admin_Settings()

    if not os.getenv(ADMIN_PASSWORD_ENV):
        print("Admin is niet ingesteld.")
        return

    password = input("Admin wachtwoord: ")
    if is_Admin_Password(password):
        print(f"Geheime code: {format_Code(secret_Code)}")
    else:
        print("Verkeerd wachtwoord.")


def get_Feedback(secret, guess):
    black_Pegs = sum(s == g for s, g in zip(secret, guess))

    # Count whites by comparing unmatched color frequencies.
    secret_Counts = {}
    guess_Counts = {}

    for s, g in zip(secret, guess):
        if s != g:
            secret_Counts[s] = secret_Counts.get(s, 0) + 1
            guess_Counts[g] = guess_Counts.get(g, 0) + 1

    white_Pegs = sum(
        min(secret_Counts.get(d, 0), guess_Counts.get(d, 0))
        for d in guess_Counts
    )

    return black_Pegs, white_Pegs


def play_Mastermind():
    print("MasterMind")
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
            raw_Guess = input(f"Poging {attempt} (A=admin): ")
            if is_Admin_Command(raw_Guess):
                admin_Menu(secret_Code)
                continue

            guess = parse_Guess(raw_Guess)
            valid_Guess = guess is not None
            if not valid_Guess:
                print("Ongeldige invoer. Voer 4 kleuren in, "
                      "bijvoorbeeld: R G B Y.")

        black, white = get_Feedback(secret_Code, guess)
        print(f"Zwarte pegs (juiste kleur en plek): {black}, "
              f"Witte pegs (juiste kleur, verkeerde plek): {white}")

        if black == 4:
            print(f"Gefeliciteerd! De code was: {format_Code(secret_Code)}")
            return

    print("Helaas, je pogingen zijn op. "
          f"De code was: {format_Code(secret_Code)}")


if __name__ == "__main__":
    again = "Y"
    while again == "Y":
        play_Mastermind()
        again = input("Nog een keer spelen (Y/N)? ").strip().upper()
