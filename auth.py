import sqlite3, flask
import json
from uuid import uuid4
from hashlib import sha256
from flask import make_response, render_template, redirect, url_for

def setupUserDB():
    con = sqlite3.connect('./db/database.db')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('''CREATE TABLE users (
        username TEXT NOT NULL, 
        password TEXT NOT NULL, 
        points INTEGER NOT NULL DEFAULT 0,
        solvedChallenges TEXT NOT NULL DEFAULT '[]'
        )''')
    con.commit()

    cur.execute('DROP TABLE IF EXISTS sessions')
    cur.execute('''CREATE TABLE sessions (
        username TEXT NOT NULL,
        token TEXT NOT NULL
        )''')
    con.commit()


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
        response.set_cookie('SESSIONID', value=token, max_age=30*60*60*24) # 30 days
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
    
    def reset_sessions(self):
        self.cur.execute('DELETE FROM sessions')
        self.con.commit()

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
                session = SessionManager('./db/database.db')
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
            self.cur.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, passwordHash))
            self.con.commit()

        except Exception as e:
            print(e)
            resp = make_response(render_template('register.html', navBarPage='register', message='There was an unexpected error. Please contact an admin.', authenticated=False))
            return resp

        # successfully registered! (set as authenticated and redirect to home)
        session = SessionManager('./db/database.db')
        resp = make_response(redirect(url_for('index')))
        resp = session.create_session(username, resp)
        return resp
    
    def checkAllowSubmit(self, username: str, challengeID: int) -> bool:
        self.cur.execute("SELECT solvedChallenges FROM users where username=?", (username,))
        result = self.cur.fetchall()[0][0]
        result = json.loads(result)
        if challengeID in result:
            return False
        else:
            return True

    def addPoints(self, username: str, points: int) -> None:
        self.cur.execute("SELECT points FROM users WHERE username=?", (username,))
        currentPoints = self.cur.fetchall()[0][0]
        self.cur.execute('UPDATE users SET points=? WHERE username=?', (currentPoints + points, username))
        self.con.commit()    
    
    def addSolvedChallenge(self, username: str, challengeID: str) -> None:
        self.cur.execute("SELECT solvedChallenges FROM users where username=?", (username,))
        result = self.cur.fetchall()[0][0]
        
        result = json.loads(result)
        result.append(challengeID)
        result = json.dumps(result)

        self.cur.execute('UPDATE users SET solvedChallenges=? WHERE username=?', (result, username))
        self.con.commit()
    
    def getPoints(self, username: str) -> int:
        self.cur.execute("SELECT points FROM users WHERE username=?", (username,))
        return self.cur.fetchall()[0][0]
    
    def getPlacing(self, username: str) -> int:
        self.cur.execute("SELECT username FROM users ORDER BY points DESC")
        results = self.cur.fetchall()
        for i in range(len(results)):
            if results[i][0] == username:
                return i + 1
        return -1 # if error
    
    def getSolvedChallenges(self, username: str) -> list:
        self.cur.execute("SELECT solvedChallenges FROM users WHERE username=?", (username,))
        return json.loads(self.cur.fetchall()[0][0])
    
    def getLeaderboard(self) -> list:
        self.cur.execute("SELECT username, points FROM users ORDER BY points DESC")
        return self.cur.fetchall()

    def resetUserSolves(self):
        self.cur.execute("UPDATE users SET solvedChallenges='[]'")
        self.cur.execute("UPDATE users SET points=0")
        self.con.commit()
    
    def deleteAllUsers(self):
        self.cur.execute("DELETE FROM users")
        self.con.commit()