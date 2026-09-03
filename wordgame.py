# Creativity: This version selects a random secret word from a list of words,
# making the game different each time it is played.

import random

print("Welcome to the word guessing game!")
print()

word_list = ["temple", "python", "banana", "school", "friend"]
secret_word = random.choice(word_list)

# Display initial hint
initial_hint = "_ " * len(secret_word)
print(f"Your hint is: {initial_hint}")
print()

guess_count = 0
guess = ""

while guess != secret_word:

    guess = input("What is your guess? ").lower()
    guess_count += 1

    if guess == secret_word:
        break

    if len(guess) != len(secret_word):
        print("Sorry, the guess must have the same number of letters as the secret word.")
        print()
        continue

    hint = ""

    for i in range(len(secret_word)):

        if guess[i] == secret_word[i]:
            hint += guess[i].upper() + " "

        elif guess[i] in secret_word:
            hint += guess[i].lower() + " "

        else:
            hint += "_ "

    print(f"Your hint is: {hint}")
    print()

print("Congratulations! You guessed it!")
print(f"It took you {guess_count} guesses.")