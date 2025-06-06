# Testing ground
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import init_db, changelog_add, statedit, database_connect, register_user, login_user, logout_user, displayInv, addToInv, statedit, delencounter, encountergen, encounterchoice, delencounter, removeFromInv
import random
import requests
import json
import mathgenerator as mg
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

@app.route('/blackjack')
def blackjack():
    return render_template("blackjack.html")

# guess the number
@app.route('/guess')
def guess():
    number = random.randint(1, 100)
    session['num'] = number
    session['previous'] = ""
    num = number
    return render_template("guess.html", number = num, prev = session['previous'].split(";"))

@app.route('/guess/check', methods = ["GET", "POST"])
def guesscheck():
    if request.method == 'POST':
        guess = (int)(request.form.get('inputNum'))
        if(guess > session['num']):
            session['previous'] = session['previous'] + ";" + (str(guess) + " was too high!")
            return render_template("guess.html", number = session['num'], prev = session['previous'].split(";"))
        if(guess < session['num']):
            session['previous'] = session['previous'] + ";" + (str(guess) + " was too low!")
            return render_template("guess.html", number = session['num'], prev = session['previous'].split(";"))
        if(guess == session['num']):
            session['previous'] = session['previous'] + ";" + ("YOU WIN WOOO!!!")
            return render_template("guess.html", number = session['num'], prev = session['previous'].split(";"), win = "wooo")
    return render_template("guess.html", number = session['num'], prev = session['previous'].split(";"))

@app.route("/rps")
def rps():
    dial = []
    oppAction = random.randint(1, 3)
    return render_template("rps.html", oppAct=oppAction, dialogue=dial, playing=True)

@app.route("/rps/check", methods=["POST"])
def rpsCheck():
    if request.method == "POST":
        action = request.form.get("inputAction")
    oppAction = random.randint(1, 3)
    if oppAction == 1:
        oppAction = "Rock"
    elif oppAction == 2:
        oppAction = "Paper"
    else:
        oppAction = "Scissors"
    win = (oppAction == "Rock" and action == "Paper") or (oppAction == "Paper" and action == "Scissors") or (oppAction == "Scissors" and action == "Rock")
    tie = oppAction == action
    return render_template("rps.html", oppAct=oppAction, act=action, won=win, tied=tie, playing=False)
'''
# hangman
@app.route('/hangman')
def hang():
    # print(displayInv('username', 'money'))
    words = ["nights", "days", "star", "rays", "supernova"]
    #global word
    word = random.choice(words)
    session['word'] = word
    #global word_letters
    word_letters = set(word)
    # Word letters being a set means that if a letter is guessed, it only has to be removed once
    # If you want to get the correct order of letters in the word, you'll want to use an array
    # For the correct letters, and reference the index position in the word string
    session['word_letters'] = word_letters
    #global correct_letters
    correct_letters = ""
    for i in range(len(word)):
        correct_letters = correct_letters + ("_")
        correct_letters = correct_letters + (" ")
    # Currently trying to create a set of letters guessed correctly, with _ for letters not discovered
    session['correct_letters'] = correct_letters
    #global alphabet
    #alphabet = set(chr(x) for x in range(ord('a'), ord('z') + 1)) # why we have built in functions
    #session['alphabet'] = alphabet
    #global used_letters
    #used_letters = set()
    session['used_letters'] = ""
    #global lives
    lives = 6
    session['lives'] = lives
    #global guessCount
    guessCount = 0
    session['guesscount'] = guessCount
    return render_template("hangman.html", lives=lives)

# To do for hangman:
# Call words from an API
# When all letters in the word are guessed, show the victory message
@app.route('/hangman/check', methods= ["GET", "POST"])
def hangcheck():
    #global word # no change
    word = session['word']
    #global word_letters # no change
    word_letters = session['word_letters']
    #global correct_letters # no change
    correct_letters = session['correct_letters']
    #global alphabet # why is it here?  no change
    #alphabet = session['alphabet']
    #global lives # change
    #global used_letters # change
    #global guessCount # change
    if request.method == 'POST':
        user_letter = request.form.get('inputLetter').lower()
        if user_letter.isalpha(): # Is it a letter?
            if user_letter not in used_letters: #Have you used it?
                guessCount += 1
                #used_letters.add(user_letter)
                if user_letter in word_letters: #Is it in the word?
                    word_letters.remove(user_letter)
                    # return the word but with the places with that letter filled out
                    for i in range(len(word)): #add it to the list of correct letters
                        if word[i] == user_letter:
                            correct_letters[i*2] = word[i]
                    if len(word_letters) == len(word): # You've guessed the word
                        return render_template("hangman.html", lives = session['lives'], used = used_letters, message="You guessed the word!", num = guessCount, c = "".join(correct_letters))
                    else:
                        return render_template("hangman.html", lives = session['lives'], used = used_letters, message="You guessed a letter!", num = guessCount, c = "".join(correct_letters))
                else:
                    session['lives'] = session['lives'] - 1
                    if session['lives'] == 0: # You've been hanged
                        return render_template("hangman.html", lives = session['lives'], used = used_letters, message="You've been hanged. Game over", num = guessCount, c = "".join(correct_letters))
                    else: # letter was not in word
                        return render_template("hangman.html", lives = session['lives'], used = used_letters, message="You suffer a penalty", num = guessCount, c = "".join(correct_letters))
            else:
                return render_template("hangman.html", lives = session['lives'], used = used_letters, message="This letter was already used", num = guessCount, c = "".join(correct_letters))
                # Say letter was already used
        else:
            return render_template("hangman.html", lives = session['lives'], used = used_letters, message="Letter is invalid", num = guessCount, c = "".join(correct_letters))
            # Invalid letter

'''

# hangman

def makeCurrent(word, guessed):
    returnable = ""
    for i in word:
        if i in guessed.split(","):
            returnable += i
        elif i == ",":
            returnable += ""
        else:
            returnable += "-"
    return returnable

@app.route('/hangman')
def hang():
    words = ["h,e,l,l,o"]
    word = random.choice(words)
    session['word'] = word
    session['usedLetters'] = ""
    session['lives'] = 6
    return render_template("hangman.html", lives = session['lives'])

@app.route('/hangman/check', methods= ["GET", "POST"])
def hangcheck():
    if request.method == 'POST':
        userInput = request.form.get('inputLetter').lower()
        if userInput.isalpha() and len(userInput) == 1:
            if userInput not in session['usedLetters'].split(","):
                session['usedLetters'] = session['usedLetters'] + "," + userInput
                if userInput in session['word'].split(","):
                    if "-" not in makeCurrent(session['word'], session['usedLetters']):
                        return render_template("hangman.html", lives = session['lives'], used = session['usedLetters'][1:], message="You guessed the word!", num = len(session['usedLetters'])/2, c = makeCurrent(session['word'], session['usedLetters']), end = True, win = True)
                    else:
                        return render_template("hangman.html", lives = session['lives'], used = session['usedLetters'][1:], message="You guessed a letter!", num = len(session['usedLetters'])/2, c = makeCurrent(session['word'], session['usedLetters']))
                else:
                    session['lives'] = session['lives'] - 1
                    if session['lives'] == 0:
                        return render_template("hangman.html", lives = session['lives'], used = session['usedLetters'][1:], message="You've been hanged. Game over", num = len(session['usedLetters'])/2, c = makeCurrent(session['word'], session['usedLetters']), lose = True)
                    else:
                        return render_template("hangman.html", lives = session['lives'], used = session['usedLetters'][1:], message="You suffer a penalty", num = len(session['usedLetters'])/2, c = makeCurrent(session['word'], session['usedLetters']))
            else:
                return render_template("hangman.html", lives = session['lives'], used = session['usedLetters'][1:], message="This letter was already used", num = len(session['usedLetters'])/2, c = makeCurrent(session['word'], session['usedLetters']))
        else:
            return render_template("hangman.html", lives = session['lives'], used = session['usedLetters'][1:], message="You sure this a letter?", num = len(session['usedLetters'])/2, c = makeCurrent(session['word'], session['usedLetters']))
    return render_template("hangman.html", lives = session['lives'])


@app.route("/scramble", methods=["GET","POST"])
def scramble():
    words = ["Placeholder"]
    word = random.choice(words)
    session["scrambleWord"] = word
    wordScramble = "".join(random.sample(word, len(word)))
    session["scrambled"] = wordScramble
    session["attempts"] = 3
    session["playing"] = True
    session["dail"] = ""
    return render_template("scramble.html", attemptsremaining = session["attempts"], scrambledWord = session["scrambled"], isPlaying = session["playing"])

@app.route("/scramble/check", methods=["POST"])
def scrambleCheck():
    if request.method == "POST":
        #print(request.form)
        guess = request.form.get("guess")
    session["attempts"]  = session["attempts"] - 1
    word = session["scrambleWord"]
    wordScramble = session["scrambled"]
    results = ""
    playing = True
    session["dail"] = session["dail"] + "You gussed " + guess + "!"
    if guess.lower() == word.lower():
        session["dail"] = session["dail"] + "Darn! It was " + word + ", you got it in " + str(int(3 - session["attempts"]))+ " attempt!;"
        results = "Won"
        playing = False
    else:
        session["dail"] = session["dail"] + "Unfortunate its wrong! Try Again!" + ";"
    if session["attempts"]  == 0:
        results = "Lost"
        playing = False
    session["playing"] = playing
    return render_template("scramble.html", attemptsremaining=session["attempts"] , scrambledWord=wordScramble, dialogue=session["dail"].split(";"), result=results, isPlaying=playing)

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
        question = item["question"]
        correct = item["correct_answer"]
        choices = item["incorrect_answers"]
        choices.insert(random.randint(0, 3), correct)

        qna[question] = correct
        questions[question] = choices
        questionList.append(question)

    # Store in session
    session["qna"] = qna
    session["questions"] = questions
    session["questionList"] = questionList

    return render_template("trivia.html", questions=questionList, answersDict=questions, numquestions=len(questionList))

@app.route("/trivia/check", methods=["POST"])
def triviaCheck():
    qna = session.get("qna", {})
    questions = session.get("questions", {})
    questionList = session.get("questionList", [])
    numQuestions = len(questionList)
    questionResults = []
    userAnswers = []
    numCorrect = 0

    if request.method == "POST":
        for i in range(numQuestions):
            answer = request.form.get(str(i))
            userAnswers.append(answer)
            correctAnswer = qna[questionList[i]]
            questionResults.append(answer == correctAnswer)

        numCorrect = questionResults.count(True)

    return render_template("triviaCheck.html", questions=questionList, correctAnswersDict=qna,
                           numquestions=numQuestions, numcorrect=numCorrect,
                           useranswers=userAnswers, answersDict=questions)

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

@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    locname = "Kitchen"
    if request.method == 'GET':
        encountername = encountergen("kitchen")
        session["encounter"] = encountername
        return render_template('encounter.html', location = "kitchen", encounter = encountername, back = "house", locname = locname)
    if request.method == 'POST':
        # Get the selected choice from the form
        encountername = session.get("encounter")
        print(encountername)
        choice = request.form.get('choice')
        return render_template('result.html', location = "kitchen", result = encounterchoice("kitchen", encountername, choice), back = "house", locname = locname)

@app.route('/bedroom', methods=['GET', 'POST'])
def bedroom():
    locname = "Bedroom"
    if request.method == 'GET':
        encountername = encountergen("bedroom")
        session["encounter"] = encountername
        return render_template('encounter.html', location = "bedroom", encounter = encountername, back = "house", locname = locname)
    if request.method == 'POST':
        # Get the selected choice from the form
        encountername = session.get("encounter")
        print(encountername)
        choice = request.form.get('choice')
        return render_template('result.html', location = "bedroom", result = encounterchoice("bedroom", encountername, choice), back = "house", locname = locname)



@app.route('/friendhouse', methods=['GET', 'POST'])
def friendhouse():
    locname = "Friend's House"
    if request.method == 'GET':
        encountername = encountergen("friendhouse")
        session["encounter"] = encountername
        return render_template('encounter.html', location = "friendhouse", encounter = encountername, back = "neighborhood", locname = locname)
    if request.method == 'POST':
        # Get the selected choice from the form
        encountername = session.get("encounter")
        print(encountername)
        choice = request.form.get('choice')
        return render_template('result.html', location = "friendhouse", result = encounterchoice("friendhouse", encountername, choice), back = "neighborhood", locname = locname)

@app.route('/park', methods=['GET', 'POST'])
def park():
    locname = "Park"
    if request.method == 'GET':
        encountername = encountergen("park")
        session["encounter"] = encountername
        return render_template('encounter.html', location = "park", encounter = encountername, back = "neighborhood", locname = locname)
    if request.method == 'POST':
        # Get the selected choice from the form
        encountername = session.get("encounter")
        print(encountername)
        choice = request.form.get('choice')
        return render_template('result.html', location = "park", result = encounterchoice("park", encountername, choice), back = "neighborhood", locname = locname)

# mall

@app.route('/candy', methods=['GET', 'POST'])
def candy():
    if request.method == 'POST':
        # Get the selected choice from the form
        selected_choice = request.form.get('choice')
        res = "You have selected: " + selected_choice + ". Thank you for your purchase!"
        return render_template('result.html', location = "candy", result = res, back = "mall", locname = "Candy Store")
    return render_template('candy.html')

@app.route('/gamble')
def gamble():
    return render_template('gamble.html')

@app.route('/darkAlley', methods=['GET', 'POST'])
def darkAlley():
    if request.method == 'POST':
        # Get the selected choice from the form
        selected_choice = request.form.get('choice')
        res = "You have selected: " + selected_choice + ". Now leave, before anyone sees you."
        return render_template('result.html', location = "darkalley", result = res, back = "mall", locname = "Dark Alley")
    return render_template('darkAlley.html')

# school

@app.route('/computerScienceLab')
def computerScienceLab():
    #3 phases 
    #hangman
    #unscramble
    #rock paper scissors
    return render_template('computerScienceLab.html')

@app.route('/screen')
def screen1():
    return render_template("screen1.html")
    
@app.route('/screen2', methods=['GET', 'POST'])
def screen2():
    return render_template("screen2.html")

@app.route('/winScreenCS')
def screen3():
    return render_template("screen3.html")
@app.route("/mathClassroom")
def mathClassroom():
    return render_template("mathClassroom.html")
@app.route("/mathFight")
def mathFight():
    difficulty = request.args.get('difficulty')

    # If difficulty is not provided, show difficulty selection only (no questions)
    if not difficulty:
        # Show difficulty selection form only, no questions yet
        return render_template("mathFight.html", show_questions=False, difficulty='medium')

    gen_pools = {
        'easy': [
            mg.addition, mg.subtraction, mg.multiplication, mg.division
        ],
        'medium': [
            mg.basic_algebra, mg.area_of_triangle, mg.quadratic_equation
        ],
        'hard': [
            mg.power_rule_differentiation, mg.power_rule_integration,
            mg.stationary_points, mg.definite_integral, mg.trig_differentiation
        ]
    }

    generators = gen_pools.get(difficulty, gen_pools['medium'])

    questionList = []
    answersDict = {}
    correctAnswers = {}
    numQuestions = 10
    max_attempts = 50
    attempts = 0

    while len(questionList) < numQuestions and attempts < max_attempts:
        attempts += 1
        gen_func = random.choice(generators)
        try:
            problem, solution = gen_func()
            # Remove $ and trim
            solution_str = str(solution).replace('$', '').strip()

            # Try to convert to int for answer choices
            base = int(float(solution_str))

            # Avoid duplicates
            if problem in questionList:
                continue

            # Generate fake answers
            fake_answers = [str(base + x) for x in [-3, -1, 1, 2] if str(base + x) != str(base)]
            choices = fake_answers[:3]
            choices.insert(random.randint(0, 3), str(base))

            questionList.append(problem)
            answersDict[problem] = choices
            correctAnswers[problem] = str(base)
        except Exception as e:
            # print(f"Skipping question due to error: {e}")
            continue

    # Store in session
    session["mathQuestions"] = questionList
    session["mathAnswers"] = correctAnswers
    session["mathChoices"] = answersDict

    return render_template("mathFight.html",
                           questions=questionList,
                           answersDict=answersDict,
                           numquestions=len(questionList),
                           difficulty=difficulty,
                           show_questions=True)


@app.route("/mathFight/check", methods=["POST"])
def mathFightCheck():
    questions = session.get("mathQuestions", [])
    correctAnswers = session.get("mathAnswers", {})
    answerChoices = session.get("mathChoices", {})
    userAnswers = []
    questionResults = []
    numCorrect = 0

    for i, question in enumerate(questions):
        userAnswer = request.form.get(str(i))
        userAnswers.append(userAnswer)
        correct = correctAnswers[question]
        questionResults.append(userAnswer == correct)

    numCorrect = questionResults.count(True)

    return render_template("mathFightCheck.html", questions=questions, correctAnswersDict=correctAnswers,
                           useranswers=userAnswers, numquestions=len(questions), numcorrect=numCorrect,
                           answersDict=answerChoices)


@app.route('/USHistory')
def USHistory():
    return render_template('USHistory.html')

@app.route('/lunchroom', methods=['GET', 'POST'])
def lunchroom():
    locname = "Lunchroom"
    if request.method == 'GET':
        encountername = encountergen("lunchroom")
        session["encounter"] = encountername
        return render_template('encounter.html', location = "lunchroom", encounter = encountername, back = "school", locname = locname)
    if request.method == 'POST':
        # Get the selected choice from the form
        encountername = session.get("encounter")
        print(encountername)
        choice = request.form.get('choice')
        return render_template('result.html', location = "lunchroom", result = encounterchoice("lunchroom", encountername, choice), back = "school", locname = locname)


if __name__ == "__main__":
    app.run(host = '0.0.0.0')
