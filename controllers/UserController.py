import sys
sys.path.append("models")
sys.path.append("lib")

from datetime import datetime, timedelta
from pybcrypt import bcrypt
from flask import session

import User

# USER CONTROL METHODS
def getUser(username=None, email=None):
    if username:
        return User.findUserByName(username)
    return User.findUserByEmail(email)

def hashUserPwd(pwd):
    newPwd = bcrypt.hashpw(pwd, bcrypt.gensalt(6))
    pwd = None
    return newPwd

def checkUserPwd(username, pwd):
    user = getUser(username)
    if user:
        hashPwd = bcrypt.hashpw(pwd, user.password)
        if hashPwd == user.password:
            pwd=None
            return True
    return False

def createNewUser(userId, username, email, pwd):
    newUser = User.initUserEntityKey(userId)
    newUser.username = username
    newUser.email = email
    newUser.password = hashUserPwd(pwd)
    try:
        newUser.put()
        return True
    except ValueError:
        pass
    return False

# SESSION CONTROL METHODS
def startUserSession(username):
    session["user"] = username
    session["start_time"] = datetime.now()
    session["refresh_time"] = session["start_time"] + timedelta(minutes=45)

def endUserSession():
    session.pop("user")
    session.pop("start_time")
    session.pop("refresh_time")

def checkSessionRefresh():
    if session.get("user") and session.get("refresh_time"):
        if datetime.now() > session["refresh_time"]:
            endUserSession()
            return True
    return False
