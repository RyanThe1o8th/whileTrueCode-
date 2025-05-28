# whileTrueCode
# 2025-01-15

# Imports
import sqlite3, os, csv
from flask import Flask, request, render_template, redirect, url_for, flash, session


app = Flask(__name__)
app.secret_key = os.urandom(32)

# database initialization
def init_db():
    """initialize db if none exists"""
    conn = sqlite3.connect('truecode.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            avatar TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            username TEXT NOT NULL,
            CURRENTHP INTEGER NOT NULL,
            TOTALHP INTEGER NOT NULL,
            INTELLIGENCE INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            itemName TEXT NOT NULL,
            itemQuant INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encounters (
            username TEXT NOT NULL,
            location TEXT NOT NULL,
            encounter TEXT NOT NULL,
            option TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS change (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            change TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def database_connect():
    if not os.path.exists('truecode.db'):
        init_db()
    conn = sqlite3.connect('truecode.db')
    return conn

#changelog
def changelog_add(message):
    with sqlite3.connect('truecode.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO change (change) VALUES (?)', (message))
        conn.commit()

# inventory display
def displayInv(username, category):
    conn = database_connect()
    cursor = conn.cursor()
    inv = cursor.execute('SELECT itemName, itemQuant FROM inventory WHERE username = ? AND category = ?', (username, category)).fetchall()
    # for each thing of a given category, I want to display all of the items and their quantities on the side
    return inv
def addToInv(username, category, name, quantity):
    conn = database_connect()
    cursor = conn.cursor()
    # What if an item has already been added to the inventory? We want to update rather than SELECT

    insertion = '''INSERT INTO inventory (username, category, itemName, itemQuant) VALUES (?, ?, ?, ?)'''
    values = (username, category, name, quantity)
    cursor.execute(insertion, values)
    conn.commit()
    print("Item added to inventory")
    cursor.close()
# def removeFromInv(username, itemName, quantity):
#
#stats
def statedit(username):
    conn = database_connect()
    cursor = conn.cursor()
    user = cursor.execute('SELECT username FROM stats WHERE username = ?', (username)).fetchone()


# User
def setup_user(user):
    try:
        with sqlite3.connect('truecode.db') as conn:
            with open('encounters.csv') as csvfile:
                cursor = conn.cursor()
                readn = csv.reader(csvfile)
                for info in readn:
                    location = info[0]
                    encounter = info[1]
                    option = info[2]
                    cursor.execute('INSERT INTO encounters (username, location, encounter, option) VALUES (?, ?, ?, ?)', (user, location, encounter, option))
                    conn.commit() #Had to move this into the loop
    except sqlite3.IntegrityError:
        flash('Database Error')


def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    # check if fields filled out
    if not username or not password or not confirm_pass:
        flash('Please fill out all fields.')

    elif password != confirm_pass:
        flash('Passwords do not match.')

    else:
        try:
            with sqlite3.connect('truecode.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password, avatar) VALUES (?, ?, ?)', (username, password, "../static/pictures/yum.png"))
                conn.commit()
                flash('User registered. Please log in.')
                setup_user(username)
                return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username already exists.')
    return redirect('/register')

def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('fill all fields')
        return redirect('/login')
    else:
        with sqlite3.connect('truecode.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            user_pass = cursor.fetchone()

            if user_pass:
                if user_pass[0] == password:
                    session['username'] = username
                    flash('logged in')
                    return redirect('/')
            else:
                flash('invalid credentials')
    return redirect('/login')

def logout_user():
    session.pop('username',)
    flash('logged out')
    return redirect('/')
