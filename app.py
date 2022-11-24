from flask import Flask, render_template, request, redirect, url_for, make_response
from hashlib import sha256
import sqlite3
from auth import SessionManager

app = Flask(__name__)

@app.route('/')
def index():
    session = SessionManager('database.db')
    check = session.get_session(request.cookies)
    if check == None: #if not logged in or if sessionID is wrong
        return render_template('index.html', navBarPage="home", authenticated=False)
    else: # if logged in
        return render_template('index.html', navBarPage="home", authenticated=True)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        session = SessionManager('database.db')
        check = session.get_session(request.cookies)
        if check == None: #if not logged in or if sessionID is wrong
            resp = make_response(render_template('login.html', navBarPage="login", authenticated=False))
            resp = session.remove_session(request.cookies, resp) 
            # clear out the session id cookie for clean login (this func also removes the token from the db but since token does not exist nothing happens)
            return resp
        else: # if logged in
            return redirect(url_for('index'))

    if request.method == "POST":
        try:
            username, passwordHash = request.form['username'], sha256(request.form['password'].encode('utf-8')).hexdigest()
        except Exception as e:
            print(e)
            return render_template('login.html', navBarPage='login', message='There was an unexpected error. Please contact an admin.', authenticated=False)
        
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("SELECT username, password FROM users WHERE username=? AND password=?", (username, passwordHash))
            results = cur.fetchall()

            if len(results) == 0:
                return render_template('login.html', navBarPage='login', message='Wrong username or password.', authenticated=False)

            elif len(results) == 1 and results[0][0] == username:
                # logged in (set as authenticated and return to home)
                session = SessionManager('database.db')
                resp = make_response(redirect(url_for('index')))
                resp = session.create_session(username, resp)
                return resp

        except Exception as e:
            print(e)
            return render_template('login.html', navBarPage='login', message='There was an unexpected error. Please contact an admin.', authenticated=False)

    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "GET":
        session = SessionManager('database.db')
        check = session.get_session(request.cookies)
        if check == None: #if not logged in or if sessionID is wrong
            resp = make_response(render_template('register.html', navBarPage="register", authenticated=False))
            resp = session.remove_session(request.cookies, resp) 
            # clear out the session id cookie for clean register (this func also removes the token from the db but since token does not exist nothing happens)
            return resp
        else: # if logged in
            return redirect(url_for('index'))

    elif request.method == "POST":
        # since this application is meant to be small I really don't mind slapping all the validation here
        username, password, passwordConfirm = request.form['username'], request.form['password'], request.form['passwordConfirm']
        if password != passwordConfirm:
            return render_template('register.html', navBarPage='register', message='Your passwords do not match. Please try again.', authenticated=False)
        
        # check for username already exists
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("SELECT username FROM users WHERE username=?", (username, ))
            if len(cur.fetchall()) != 0:
                return render_template('register.html', navBarPage='register', message='Invalid username.', authenticated=False)

        except Exception as e:
            print(e)
            return render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False)
        
        try:
            passwordHash = sha256(password.encode('utf-8')).hexdigest()
        except Exception as e:
            print(e)
            return render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False)
        
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO users VALUES(?, ?)", (username, passwordHash))
            con.commit()

        except Exception as e:
            print(e)
            return render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False)
        
        # successfully registered! (set as authenticated and redirect to home)
        session = SessionManager('database.db')
        resp = make_response(redirect(url_for('index')))
        resp = session.create_session(username, resp)
        return resp

@app.route('/challenges')
def challenge():
    session = SessionManager('database.db')
    check = session.get_session(request.cookies)
    if check == None: #if not logged in or if sessionID is wrong
        return redirect(url_for('login'))
    else:
        return render_template('challengeGallery.html', navBarPage="challenges", authenticated=True)

app.run(port=5000, host='0.0.0.0', debug=True)