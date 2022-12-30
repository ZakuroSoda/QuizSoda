from flask import render_template_string, make_response
from auth import SessionManager, AccountManager
from challenges import assembleChallengePage, initDatabaseFromFiles

def resetAll():
    ''' DANGEROUS USE WITH CAUTION'''
    # reloads the CHALLENGE database from the CHALLENGES directory, clears solves per challenge
    initDatabaseFromFiles()
    # REMOVES ALL SESSIONS
    session = SessionManager('./db/database.db')
    session.reset_sessions()
    # REMOVES ALL POINTS AND ALL SOLVE RECORDS PER USER
    account = AccountManager('./db/database.db')
    account.resetUserSolves()
    # REMOVES ALL USERS
    account.deleteAllUsers()

def checkLoggedIn(request):
    session = SessionManager('./db/database.db')
    check = session.get_session(request.cookies)
    if check == None: #if not logged in or if sessionID is wrong
        return False
    else:
        return check

def fullAssembleChallengePage(username: str, alertType=None, alertMessage=None):
    webpage = assembleChallengePage()

    account = AccountManager('./db/database.db')
    solvedChallenges = account.getSolvedChallenges(username)

    resp = make_response(render_template_string(webpage, navBarPage="challenges", authenticated=True, solvedChallenges=solvedChallenges, alertType=alertType, alertMessage=alertMessage))
    return resp