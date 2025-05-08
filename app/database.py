 # Nia Lam, Amanda Tan, Naomi Lai, Kishi Wijaya
# Magical Magnolias
# SoftDev
# P02: Makers Makin' It, Act I
# 2025-01-15

# Imports
import sqlite3, os, csv
from flask import Flask, request, render_template, redirect, url_for, flash, session


app = Flask(__name__)
app.secret_key = os.urandom(32)

# database initialization
def init_db():
    """initialize db if none exists"""
    conn = sqlite3.connect('magnolia.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            CURRENTHP INTEGER NOT NULL,
            TOTALHP INTEGER NOT NULL,
            INTELLIGENCE INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def database_connect():
    if not os.path.exists('magnolia.db'):
        init_db()
    conn = sqlite3.connect('magnolia.db')
    return conn

database_connect()

# User
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_pass')

    if not username or not password or not confirm_pass:
        flash('fill all fields')
    elif password != confirm_pass:
        flash('passwords dont match')
    else:
        try:
            with sqlite3.connect('magnolia.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
                cursor.execute('INSERT INTO stats (user, magicpower, flowerscore, day) VALUES (?,?,?,?)', (username, 1, 1, 1))
                conn.commit()
                flash('registered')
        except sqlite3.IntegrityError:
            flash('username already exists')
    return redirect('/login')

def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('fill all fields')
        return redirect('/login')
    else:
        with sqlite3.connect('magnolia.db') as conn:
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
    return redirect('/login')


# Shop -> access flower db for info
def get_flower():
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT * FROM flower_base').fetchall()
            return result
    except sqlite3.IntegrityError:
        flash('error')

def purchase():
    purchase_info = request.form.get('purchase_info')
    purchase_info = list(map(int, purchase_info.split('###')))
    flower_id = purchase_info[0]
    cost = purchase_info[1]
    username = session['username']

    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT magicpower, flowerscore FROM stats WHERE user = ?', (username,)).fetchone()
            magicpower = result[0]
            flowerscore = result[1]

            if flowerscore >= flower_id:
                if magicpower >= cost:                    
                    flash('user can buy')
                    buy(username, flower_id, 0)
                else:                    
                    flash('not enough magic power. play minigames to earn more!')
            else:
                # comment after, for testing purposes
                buy(username, flower_id, 0)
                flash('flower not unlocked')
    except sqlite3.IntegrityError:
        flash('error')
    return redirect('shop')

def buy(username, flower_id, cost):
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            quantity = cursor.execute('SELECT quantity FROM seeds WHERE user = ? AND flower_id = ?', (username,flower_id)).fetchone()
            if not quantity:
                quantity = 0
                cursor.execute('INSERT INTO seeds (user, flower_id, quantity) VALUES (?, ?, 0)', (username, flower_id,))
            else:
                quantity = quantity[0]            
            cursor.execute('UPDATE seeds SET quantity = ? WHERE user = ? AND flower_id = ?', (quantity + 1, username, flower_id))
            cursor.execute('UPDATE stats SET magicpower = magicpower - ? WHERE user = ?', (cost, username))
    except sqlite3.IntegrityError:
        flash('error')

# Game
def inc_mp(n):
    username = session['username']
    try:
        with sqlite3.connect('magnolia.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE stats SET magicpower = magicpower + ? WHERE user = ?', (n, username))
    except sqlite3.IntegrityError:
        flash('error')
