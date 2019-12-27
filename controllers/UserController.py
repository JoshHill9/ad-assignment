import sys
sys.path.append("models")
sys.path.append("lib")

from datetime import datetime, timedelta
from pybcrypt import bcrypt
from flask import session
import User
import random

# USER CONTROL METHODS
def get_user(user_id=None, username=None, email=None):
    if user_id:
        return User.find_by_id(user_id)
    elif username:
        return User.find_user_by_name(username)
    elif email:
        return User.find_user_by_email(email)

def hash_user_pwd(pwd):
    newPwd = bcrypt.hashpw(pwd, bcrypt.gensalt(6))
    pwd = None
    return newPwd

def check_user_pwd(username, pwd):
    user = get_user(username=username)
    if user:
        hashPwd = bcrypt.hashpw(pwd, user.password)
        if hashPwd == user.password:
            pwd=None
            return True
    return False

def create_new_user(user_id, username, email, pwd, joined_from):
    newUser = None
    if user_id == "auto_gen":
        auto_id = username + str(random.randint(0,1000))
        while get_user(user_id=auto_id):
            auto_id = username + str(randint(0,1000))
        newUser = User.init_user_entity_key(auto_id)
        newUser.user_id = auto_id
    else:
        newUser = User.init_user_entity_key(user_id)
        newUser.user_id = user_id

    newUser.username = username
    newUser.email = email
    newUser.password = hash_user_pwd(pwd)
    newUser.joined_from = joined_from
    try:
        newUser.put()
        return True
    except ValueError:
        pass
    return False


# SESSION CONTROL METHODS
def start_user_session(username, user_type="website_user"):
    session["user"] = username
    session["user_type"] = user_type
    session["start_time"] = datetime.now()
    session["refresh_time"] = session["start_time"] + timedelta(minutes=45)

def end_user_session():
    session.pop("user")
    session.pop("start_time")
    session.pop("refresh_time")

def check_session_refresh():
    if session.get("user") and session.get("refresh_time"):
        if datetime.now() > session["refresh_time"]:
            end_user_session()
            return True
    return False
