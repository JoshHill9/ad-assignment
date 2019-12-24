import sys
sys.path.append("models")
sys.path.append("lib")

from datetime import datetime, timedelta
from pybcrypt import bcrypt
from flask import session
import random
import User

# USER CONTROL METHODS
def getUser(user_id=None, username=None, email=None):
    if user_id:
        return find_by_id(user_id)
    elif username:
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

def createNewUser(user_id, username, email, pwd, joined_from):
    newUser = None
    if user_id == "auto_gen":
        auto_id = username + str(randint(0,1000))
        while getUser(user_id=auto_id):
            auto_id = username + str(randint(0,1000))
        newUser = User.initUserEntityKey(auto_id)
    else:
        newUser = User.initUserEntityKey(user_id)

    newUser.username = username
    newUser.email = email
    newUser.password = hashUserPwd(pwd)
    newUser.joined_from = joined_from
    try:
        newUser.put()
        return True
    except ValueError:
        pass
    return False

# SESSION CONTROL METHODS
def startUserSession(username, user_type="website_user"):
    session["user"] = username
    session["user_type"] = user_type
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
