# Testing ground
from flask import Flask, redirect, session, render_template, url_for, request

app = Flask(__name__)
app.secret_key = 'whileTrueCode()-'

@app.route('/')
def root():
    return render_template("home.html", user=session.get('username'))

@app.route('/testing')
def testing():
    return render_template("testing.html", user=session.get('username'))

if __name__ == "__main__":
    app.run()
