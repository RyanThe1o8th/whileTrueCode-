# Testing ground
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import init_db, database_connect, register_user, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'whileTrueCode()-'

database_connect()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', username = session.get('username'))

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
    return render_template('profile.html', username = session.get('username'))


@app.route('/testing')
def testing():
    return render_template("testing.html", user=session.get('username'))

// subway travel

@app.route('/subway')
def mainHome():
    return render_template('home.html')

@app.route('/neighborhood')
def mainHome():
    return render_template('neighborhood.html')

@app.route('/mall')
def mainHome():
    return render_template('mall.html')

@app.route('/school')
def mainHome():
    return render_template('school.html')

// neighborhood

@app.route('/home')
def mainHome():
    return render_template('mhome.html')

@app.route('/friendHouse')
def mainHome():
    return render_template('friendHouse.html')

@app.route('/park')
def mainHome():
    return render_template('park.html')

// mall

@app.route('/candy')
def mainHome():
    return render_template('candy.html')

@app.route('/gamble')
def mainHome():
    return render_template('gamble.html')

@app.route('/darkAlley')
def mainHome():
    return render_template('darkAlley.html')

// school

@app.route('/computerScienceLab')
def mainHome():
    return render_template('computerScienceLab.html')

@app.route('/mathClassroom')
def mainHome():
    return render_template('mathClassroom.html')

@app.route('/USHistory')
def mainHome():
    return render_template('USHistory.html')

@app.route('/lunchroom')
def mainHome():
    return render_template('lunchroom.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
