import random

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
if __name__ == "__main__":
    play_blackjack()
