import sqlite3, flask
from uuid import uuid4
from hashlib import sha256
from flask import make_response, render_template, redirect, url_for

class SessionManager:
    def __init__(self, instance):
        self.con = sqlite3.connect(f'{instance}')
        self.cur = self.con.cursor()
    
    def create_session(self, username: str, response: flask.Response) -> flask.Response:
        while True:
            token = uuid4().hex
            self.cur.execute('SELECT token FROM sessions WHERE token=?', (token,))
            result = self.cur.fetchall()
            if len(result) == 0:
                break
        self.cur.execute('INSERT INTO sessions VALUES (?, ?)', (username, token))
        self.con.commit()
        response.set_cookie('SESSIONID', token)
        return response
    
    def get_session(self, cookies):
        sessionID = cookies.get('SESSIONID')
        if sessionID == None:
            return None

        self.cur.execute('SELECT username FROM sessions WHERE token=?', (sessionID,))
        result = self.cur.fetchall()

        if len(result) == 0:
            return None
        else:
            return result[0][0]
            
    def remove_session(self, cookies: flask.Request.cookies, response: flask.Response) -> flask.Response:
        sessionID = cookies.get('SESSIONID')
        if sessionID == None:
            return response
        self.cur.execute('DELETE FROM sessions WHERE token=?', (sessionID, ))
        self.con.commit()
        response.set_cookie('SESSIONID', '', expires=0)
        return response

class AccountManager:
    def __init__(self, instance):
        self.con = sqlite3.connect(f'{instance}')
        self.cur = self.con.cursor()
    
    def login(self, request: flask.Request) -> flask.Response:
        try:
            username, passwordHash = request.form['username'], sha256(request.form['password'].encode('utf-8')).hexdigest()
        except Exception as e:
            print(e)
            resp = make_response(render_template('login.html', navBarPage='login', message='There was an unexpected error. Please contact an admin.', authenticated=False))
            return resp
        
        try:
            self.cur.execute("SELECT username, password FROM users WHERE username=? AND password=?", (username, passwordHash))
            results = self.cur.fetchall()

            if len(results) == 0:
                resp = make_response(render_template('login.html', navBarPage='login', message='Wrong username or password.', authenticated=False))
                return resp

            elif len(results) == 1 and results[0][0] == username:
                # logged in (set as authenticated and return to home)
                session = SessionManager('database.db')
                resp = make_response(redirect(url_for('index')))
                resp = session.create_session(username, resp)
                return resp

        except Exception as e:
            print(e)
            resp = make_response(render_template('login.html', navBarPage='login', message='There was an unexpected error. Please contact an admin.', authenticated=False))
            return resp
    
    def register(self, request: flask.Request) -> flask.Response:

        username, password, passwordConfirm = request.form['username'], request.form['password'], request.form['passwordConfirm']
        if password != passwordConfirm:
            resp = make_response(render_template('register.html', navBarPage='register', message='Your passwords do not match. Please try again.', authenticated=False))
            return resp
        
        # check for username already exists
        try:
            self.cur.execute("SELECT username FROM users WHERE username=?", (username, ))
            if len(self.cur.fetchall()) != 0:
                resp = make_response(render_template('register.html', navBarPage='register', message='Invalid username.', authenticated=False))
                return resp

        except Exception as e:
            print(e)
            resp = make_response(render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False))
            return resp
        
        try:
            passwordHash = sha256(password.encode('utf-8')).hexdigest()
        except Exception as e:
            print(e)
            resp = make_response(render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False))
            return resp
        
        try:
            self.cur.execute("INSERT INTO users VALUES(?, ?)", (username, passwordHash))
            self.con.commit()

        except Exception as e:
            print(e)
            resp = make_response(render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False))
            return resp

        # successfully registered! (set as authenticated and redirect to home)
        session = SessionManager('database.db')
        resp = make_response(redirect(url_for('index')))
        resp = session.create_session(username, resp)
        return resp