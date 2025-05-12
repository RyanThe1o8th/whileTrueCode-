import random

words = ["python", "programming", "algorithm", "data", "structure", "analysis", "science", "statistic"]

def word_scrambled(word):
    word_scrambled = ''.join(random.sample(word, len(word)))
    return word_scrambled

score = 0
attempts = 0

while True:
    # Select a word and scramble it
    selected_word = random.choice(words)

    # Set the maximum number of attempts
    max_attempts = 3

    # Start the guessing loop
    while attempts < max_attempts:
        guess = input("Guess the scrambled word: " + word_scrambled(selected_word))  # Remove the second call to word_scrambled

        # Check if the guess is correct
        if guess == selected_word:
            score += 1
            attempts += 1
            print("Correct! You guessed the word in " + str(attempts) + " attempts.")
            break

        else:
            attempts += 1
            print("Incorrect. Try again.")

    # Handle the case of reaching the maximum number of attempts
    if attempts == max_attempts:
        print("Game Over! You ran out of attempts. The correct word was: " + selected_word)
        break

    # Allow the user to continue or quit
    play_again = input("Play again? (Y/N): ")
    if play_again.lower() != "y":
        print("Thank you for playing! Your final score is: " + str(score))
        break





