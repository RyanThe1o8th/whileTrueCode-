import random
import time

def shuffle_cards():
    cards = ["A", "B", "C"]
    random.shuffle(cards)
    return cards

def display_cards(cards):
    print("Here are the cards:")
    print("A  B  C")
    print(cards)

def get_player_choice():
  while True:
    choice = input("Choose a card (A, B, or C): ").upper()
    if choice in ['A', 'B', 'C']:
      return choice
    else:
      print("Invalid choice. Please choose A, B, or C.")

def reveal_card(cards, player_choice):
    card_index = {'A': 0, 'B': 1, 'C': 2}[player_choice]
    if cards[card_index] == "B":
        print("Congratulations! You found the B!")
        return True
    else:
        print("Sorry, that's not the B. It was at position:", cards.index("B") + 1)
        return False

def play_game():
    cards = shuffle_cards()
    display_cards(cards)
    time.sleep(2)  # Briefly show cards
    print("\n" * 50) #Clear the screen
    print("Shuffling...")
    time.sleep(1)

    player_choice = get_player_choice()
    reveal_card(cards, player_choice)

if __name__ == "__main__":
    play_game()
