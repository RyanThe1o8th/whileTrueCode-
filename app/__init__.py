# Testing ground
from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from database import init_db, changelog_add, statedit, database_connect, register_user, login_user, logout_user
import game


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
