from flask import Flask, render_template, request, redirect, url_for
from hashlib import sha256
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', navBarPage="home")

@app.route('/login')
def login():
    return render_template('login.html', navBarPage="login")
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "GET":
        #if not logged in
        return render_template('register.html', navBarPage="register")
        #if logged in
            # redirect to home
    elif request.method == "POST":
        # since this application is meant to be small I really don't mind slapping all the validation here
        username, password, passwordConfirm = request.form['username'], request.form['password'], request.form['passwordConfirm']
        if password != passwordConfirm:
            return render_template('register.html', navBarPage='register', message='Your passwords do not match. Please try again.')
        
        # check for username already exists
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("SELECT username FROM users WHERE username=?", (username, ))
            if len(cur.fetchall()) != 0:
                return render_template('register.html', navBarPage='register', message='Invalid username.')

        except Exception as e:
            print(e)
            return render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.')
        
        try:
            passwordHash = sha256(password.encode('utf-8')).hexdigest()
        except Exception as e:
            print(e)
            return render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.')
        
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO users VALUES(?, ?)", (username, passwordHash))
            con.commit()
        except Exception as e:
            print(e)
            return render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.')
        
        # successfully registered! (set as authenticated and redirect to home)
        return 'test'

@app.route('/challenges')
def challenge():
    return render_template('challengeGallery.html', navBarPage="challenges")

app.run(port=5000, host='0.0.0.0')