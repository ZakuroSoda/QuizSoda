import sqlite3, flask
from uuid import uuid4

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
            
    def remove_session(self, cookies, response: flask.Response) -> flask.Response:
        sessionID = cookies.get('SESSIONID')
        if sessionID == None:
            return response
        self.cur.execute('DELETE FROM sessions WHERE token=?', (sessionID, ))
        self.con.commit()
        response.set_cookie('SESSIONID', '', expires=0)
        return response
        