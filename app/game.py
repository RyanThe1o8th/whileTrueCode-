import random

# Blackjack
def deal_card(deck):
    return deck.pop()

def calculate_hand_value(hand):
    ace_count = hand.count('A')
    total = 0
    for card in hand:
        if card.isdigit():
            total += int(card)
        elif card in ('J', 'Q', 'K'):
            total += 10
        elif card == 'A':
            total += 11
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total

def display_hands(player_hand, dealer_hand, show_dealer=False):
    print("\nDealer's Hand:")
    if show_dealer:
        print(*dealer_hand)
        print("Value:", calculate_hand_value(dealer_hand))
    else:
        print("[hidden]", *dealer_hand[1:])
    print("\nYour Hand:")
    print(*player_hand)
    print("Value:", calculate_hand_value(player_hand))

def play_blackjack():
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    deck = [rank for rank in ranks for suit in suits] * 4
    random.shuffle(deck)
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    while True:
        display_hands(player_hand, dealer_hand)
        if calculate_hand_value(player_hand) == 21:
            print("\nBlackjack! You win!")
            break
        action = input("\nHit or Stand? (h/s): ").lower()
        if action == 'h':
            player_hand.append(deal_card(deck))
            if calculate_hand_value(player_hand) > 21:
                display_hands(player_hand, dealer_hand, show_dealer=True)
                print("\nBust! You lose.")
                break
        elif action == 's':
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deal_card(deck))
            display_hands(player_hand, dealer_hand, show_dealer=True)
            if calculate_hand_value(dealer_hand) > 21 or calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
                print("\nYou win!")
            elif calculate_hand_value(player_hand) == calculate_hand_value(dealer_hand):
                print("\nPush! It's a tie.")
            else:
                print("\nYou lose.")
            break

# Number guessing game
def guess_the_number():
    number = random.randint(1, 100)
    attempts = 0

    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Take a guess: "))
            attempts += 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if guess < number:
            print("Too low!")
        elif guess > number:
            print("Too high!")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            break

# hangman
def hangman():
    words = ["python", "java", "javascript", "ruby", "swift", "kotlin"]
    word = random.choice(words)
    word_letters = set(word)
    alphabet = set(chr(x) for x in range(ord('a'), ord('z') + 1))
    used_letters = set()

    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print("You have", lives, "lives left and have used these letters: ", ' '.join(used_letters))

        word_list = [letter if letter in used_letters else '-' for letter in word]
        print("Current word: ", ' '.join(word_list))

        user_letter = input("Guess a letter: ").lower()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives -= 1
                print("Letter is not in word.")

        elif user_letter in used_letters:
            print("You have already used that character. Please try again.")

        else:
            print("Invalid character. Please try again.")

    if lives == 0:
        print("You died, sorry. The word was", word)
    else:
        print("You guessed the word", word, "!!")

# Rock paper scissors
def play():
    user_action = input("Enter a choice (rock, paper, scissors): ")
    possible_actions = ["rock", "paper", "scissors"]
    computer_action = random.choice(possible_actions)
    print(f"\nYou chose {user_action}, computer chose {computer_action}.\n")

    if user_action == computer_action:
        print(f"Both players selected {user_action}. It's a tie!")
    elif user_action == "rock":
        if computer_action == "scissors":
            print("Rock smashes scissors! You win!")
        else:
            print("Paper covers rock! You lose.")
    elif user_action == "paper":
        if computer_action == "rock":
            print("Paper covers rock! You win!")
        else:
            print("Scissors cuts paper! You lose.")
    elif user_action == "scissors":
        if computer_action == "paper":
            print("Scissors cuts paper! You win!")
        else:
            print("Rock smashes scissors! You lose.")
    else:
        print("Invalid input. Please choose rock, paper, or scissors.")

# Implement the other three later

if __name__ == "__main__":
    pass
    # play_blackjack()
