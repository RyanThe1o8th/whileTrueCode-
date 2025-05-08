# Testing ground
from flask import Flask, redirect, session, render_template, url_for, request

app = Flask(__name__)
app.secret_key = 'whileTrueCode()-'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/login')
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If form info is from register, register the user; if info from login, user logs in
    if request.method == 'POST':
        if request.form.get('register'):
            return register_user()
        if request.form.get('login'):
            return login_user()
        else:
            flash('form error')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user()

@app.route('/testing')
def testing():
    return render_template("testing.html", user=session.get('username'))

if __name__ == "__main__":
    app.run()
