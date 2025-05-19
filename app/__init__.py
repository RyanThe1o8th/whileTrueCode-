# Testing ground
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import init_db, changelog_add, statedit, database_connect, register_user, login_user, logout_user
import game
import random


app = Flask(__name__)
app.secret_key = 'whileTrueCode()-'

database_connect()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', username = session.get('username'), changelog = session.get('change'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If form info is from register, register the user; if info from login, user logs in
    if request.method == 'POST':
        if request.form.get('login'):
            return login_user()
        else:
            flash('form error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # If form info is from register, register the user; if info from login, user logs in
    if request.method == 'POST':
        if request.form.get('register'):
            return register_user()
        else:
            flash('form error')
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user()

@app.route('/profile', methods=['Get', 'POST'])
def profile():
    return render_template('profile.html', username = session.get('username'), avatar = session.get('avatar'))


@app.route('/testing')
def testing():
    return render_template("testing.html", user=session.get('username'))

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

running_deck = "placeholder"
player = "a"
dealer = "b"

@app.route('/blackjack')
def blackjack():
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    deck = [rank for rank in ranks for suit in suits] * 4
    random.shuffle(deck)
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    global running_deck
    global player
    global dealer
    running_deck = deck
    player = player_hand
    dealer = dealer_hand
    print(*player_hand)
    print(*dealer_hand)
    return render_template("blackjack.html", player = player_hand, dealer = dealer_hand, player_value = calculate_hand_value(player_hand), dealer_value = calculate_hand_value(dealer_hand))

@app.route('/blackjack/stand')
def blackjackStand():
    global running_deck
    global player
    global dealer
    deck = running_deck
    player_hand = player
    dealer_hand = dealer
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        if calculate_hand_value(dealer_hand) > 21 or calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
            return render_template("blackjack.html", player = player_hand, dealer = dealer_hand, player_value = calculate_hand_value(player_hand), dealer_value = calculate_hand_value(dealer_hand), result = "You won!!!")
        elif calculate_hand_value(player_hand) == calculate_hand_value(dealer_hand):
            return render_template("blackjack.html", player = player_hand, dealer = dealer_hand, player_value = calculate_hand_value(player_hand), dealer_value = calculate_hand_value(dealer_hand), result = "Push. Oh well.")
        else:
            return render_template("blackjack.html", player = player_hand, dealer = dealer_hand, player_value = calculate_hand_value(player_hand), dealer_value = calculate_hand_value(dealer_hand), result = "Loser")

@app.route('/blackjack/hit')
def blackjackHit():
    global running_deck
    global player
    global dealer
    deck = running_deck
    player.append(deal_card(deck))
    player_hand = player
    dealer_hand = dealer
    return render_template("blackjack.html", player = player_hand, dealer = dealer_hand, player_value = calculate_hand_value(player_hand), dealer_value = calculate_hand_value(dealer_hand))
#blackjack()

# subway

@app.route('/subway')
def subway():
    return render_template('subway.html')

@app.route('/neighborhood')
def neighborhood():
    return render_template('neighborhood.html')

@app.route('/mall')
def mall():
    return render_template('mall.html')

@app.route('/school')
def school():
    return render_template('school.html')

# neighborhood

@app.route('/house')
def house():
    return render_template('house.html')

@app.route('/friendHouse')
def friendHouse():
    return render_template('friendHouse.html')

@app.route('/park')
def park():
    return render_template('park.html')

# mall

@app.route('/candy')
def candy():
    return render_template('candy.html')

@app.route('/gamble')
def gamble():
    return render_template('gamble.html')

@app.route('/darkAlley')
def darkAlley():
    return render_template('darkAlley.html')

# school

@app.route('/computerScienceLab')
def computerScienceLab():
    return render_template('computerScienceLab.html')

@app.route('/mathClassroom')
def mathClassroom():
    return render_template('mathClassroom.html')

@app.route('/USHistory')
def USHistory():
    return render_template('USHistory.html')

@app.route('/lunchroom')
def lunchroom():
    return render_template('lunchroom.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
