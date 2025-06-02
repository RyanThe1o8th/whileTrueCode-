# Testing ground
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import init_db, changelog_add, statedit, database_connect, register_user, login_user, logout_user, displayInv, addToInv, statedit, delencounter, encountergen
import game
import random
import requests
import json

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

# guess the number

num = 0
previous = []

@app.route('/guess')
def guess():
    number = random.randint(1, 100)
    global num
    global previous
    num = number
    return render_template("guess.html", number = num, prev = previous)

@app.route('/guess/check', methods = ["GET", "POST"])
def guesscheck():
    global num
    global previous
    if request.method == 'POST':
        guess = (int)(request.form.get('inputNum'))
        if(guess > num):
            previous.append(str(guess) + " was too high!")
            return render_template("guess.html", number = num, prev = previous)
        if(guess < num):
            previous.append(str(guess) + " was too low!")
            return render_template("guess.html", number = num, prev = previous)
        if(guess == num):
            previous.append("YOU WIN WOOO!!!")
            return render_template("guess.html", number = num, prev = previous, win = "wooo")
    return render_template("guess.html", number = num, prev = previous)

@app.route("/rps")
def rps():
    global oppAction
    dial = []
    oppAction = random.randint(1, 3)

    return render_template("rps.html", oppAct=oppAction, dialogue=dial, playing=True)

@app.route("/rps/check", methods=["POST"])
def rpsCheck():
    if request.method == "POST":
        action = request.form.get("inputAction")
        # print(action)

    global oppAction
    global dial
    dial = []
    oppAction = random.randint(1, 3)

    if oppAction == 1:
        oppAction = "Rock"
    elif oppAction == 2:
        oppAction = "Paper"
    else:
        oppAction = "Scissors"


    print(f"Player Action: {action}, Opponent Action: {oppAction}")
    # addToInv('username', 'money', 'dollars', 10)
    # print(displayInv('username', 'money'))
    #Win Cons
    win = (oppAction == "Rock" and action == "Paper") or (oppAction == "Paper" and action == "Scissors") or (oppAction == "Scissors" and action == "Rock")
    tie = oppAction == action

    return render_template("rps.html", oppAct=oppAction, act=action, won=win, tied=tie, playing=False)

# hangman
@app.route('/hangman')
def hang():
    # print(displayInv('username', 'money'))
    words = ["nights", "days", "stars", "rays", "supernova", "super mega ultra hyper explosion"]
    global word
    word = random.choice(words)
    global word_letters
    word_letters = set(word)
    # Word letters being a set means that if a letter is guessed, it only has to be removed once
    # If you want to get the correct order of letters in the word, you'll want to use an array
    # For the correct letters, and reference the index position in the word string
    global correct_letters
    correct_letters = []
    for i in range(len(word)):
        correct_letters.append("_")
        correct_letters.append(" ")
    # Currently trying to create a set of letters guessed correctly, with _ for letters not discovered
    global alphabet
    alphabet = set(chr(x) for x in range(ord('a'), ord('z') + 1))
    global used_letters
    used_letters = set()
    global lives
    lives = 6
    global guessCount
    guessCount = 0
    return render_template("hangman.html", lives=lives)

# To do for hangman:
# Call words from an API
# When all letters in the word are guessed, show the victory message
@app.route('/hangman/check', methods= ["GET", "POST"])
def hangcheck():
    global word
    global word_letters
    global used_letters
    global correct_letters
    global lives
    global alphabet
    global guessCount
    if request.method == 'POST':
        user_letter = request.form.get('inputLetter').lower()
        if user_letter in alphabet: # Is it a letter?
            if user_letter not in used_letters: #Have you used it?
                guessCount += 1
                used_letters.add(user_letter)
                if user_letter in word_letters: #Is it in the word?
                    word_letters.remove(user_letter)
                    # return the word but with the places with that letter filled out
                    for i in range(len(word)): #add it to the list of correct letters
                        if word[i] == user_letter:
                            correct_letters[i*2] = word[i]
                    if len(word_letters) == len(word): # You've guessed the word
                        return render_template("hangman.html", lives = lives, used = used_letters, message="You guessed the word!", num = guessCount, c = "".join(correct_letters))
                    else:
                        return render_template("hangman.html", lives = lives, used = used_letters, message="You guessed a letter!", num = guessCount, c = "".join(correct_letters))
                else:
                    lives -= 1
                    if lives == 0: # You've been hanged
                        return render_template("hangman.html", lives = lives, used = used_letters, message="You've been hanged. Game over", num = guessCount, c = "".join(correct_letters))
                    else: # letter was not in word
                        return render_template("hangman.html", lives = lives, used = used_letters, message="You suffer a penalty", num = guessCount, c = "".join(correct_letters))
            else:
                return render_template("hangman.html", lives = lives, used = used_letters, message="This letter was already used", num = guessCount, c = "".join(correct_letters))
                # Say letter was already used
        else:
            return render_template("hangman.html", lives = lives, used = used_letters, message="Letter is invalid", num = guessCount, c = "".join(correct_letters))
            # Invalid letter



@app.route("/scramble", methods=["GET","POST"])
def scramble():
    global word
    global wordScramble
    global attemptsR
    global playing

    word = "Placeholder"
    wordScramble = "".join(random.sample(word, len(word)))
    attemptsR = 3
    playing = True



    return render_template("scramble.html", attemptsremaining=attemptsR, scrambledWord=wordScramble, isPlaying=playing)

@app.route("/scramble/check", methods=["POST"])
def scrambleCheck():
    if request.method == "POST":
        print(request.form)
        guess = request.form.get("guess")

    global word
    global wordScramble
    global attemptsR
    global playing
    global dial

    attemptsR = attemptsR - 1
    word = word
    wordScramble = wordScramble
    dial = []
    results = "Unknown"

    dial.append(f"You gussed {guess}!")

    if guess.lower() == word.lower():
        dial.append(f"Darn! It was {word}, you got it in {3 - attemptsR}!")
        results = "Won"
        playing = False
    else:
        dial.append("HAHA you suck! Try Again!")

    if attemptsR == 0:
        results = "Lost"
        playing = False

    return render_template("scramble.html", attemptsremaining=attemptsR, scrambledWord=wordScramble, dialogue=dial, result=results, isPlaying=playing)

@app.route("/trivia")
def trivia():
    response = requests.get("https://opentdb.com/api.php?amount=10&category=23&type=multiple")
    data = response.json()
    qna = {} #Store question and answer pairs
    questions = {} #Store question and multiple choice answers
    questionList = []
    numQuestions = 0
    # print(data)
    for item in data["results"]:
        # print (item["question"])
        # print (item["correct_answer"])
        # print (item["incorrect_answers"])
        # print(item["incorrect_answers"].append(item["correct_answer"]))


        qna[item["question"]] = item["correct_answer"]
        questions[item["question"]] = item["incorrect_answers"]
        questions[item["question"]].insert(random.randint(0, 3), item["correct_answer"])

        questionCurrent = item["question"]
        questionAnswer = qna[item["question"]]
        questionChoices = questions[item["question"]]
        questionList.append(questionCurrent)

        print(f"Question: {questionCurrent}, Answer: {questionAnswer}")
        print(f"Question: {questionCurrent}, Answer Choices: {questionChoices}")
        print(questionList)

    numQuestions = len(questionList)

    return render_template("trivia.html", questions=questionList, answersDict=questions, numquestions=numQuestions)

@app.route("/trivia/check", methods=["POST"])
def triviaCheck():
    if request.method == "POST":
        print(request.form)

    return "aaa"

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

def kitchen():
    encountername = encountergen("Kitchen")
    return render_template('encounter.html', location = "Kitchen", encounter = encountername, back = "house")

def bedroom():
    encountername = encountergen("Bedroom")
    return render_template('encounter.html', location = "Bedroom", encounter = encountername, back = "house")


@app.route('/friendHouse')
def friendHouse():
    encountername = encountergen("Friend's House")
    return render_template('encounter.html', location = "FHouse", encounter = encountername, back = "neighborhood")

@app.route('/park')
def park():
    encountername = encountergen("Park")
    return render_template('encounter.html', location = "Park", encounter = encountername, back = "neighborhood")

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
    encountername = encountergen("Lunchroom")
    return render_template('encounter.html', location = "Lunchroom", encounter = encountername, back = "school")

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
