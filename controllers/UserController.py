import sys
sys.path.append("models")
sys.path.append("lib")

from datetime import datetime, timedelta
from pybcrypt import bcrypt
from flask import session
import User
import random

def get_user(user_id=None, username=None, email=None):
    if user_id:
        return User.get_by_id(user_id)
    elif username:
        return User.get_by_username(username)
    elif email:
        return User.get_by_email(email)

def hash_user_pwd(pwd):
    new_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt(6))
    pwd = None
    return new_pwd

def check_user_pwd(username, pwd):
    user = get_user(username=username)
    if user:
        hash_pwd = bcrypt.hashpw(pwd, user.password)
        if hash_pwd == user.password:
            pwd=None
            return True
    return False

def generate_user_id(username):
    user_id = username + str(random.randint(0,1000))
    while get_user(user_id=user_id):
        user_id = username + str(random.randint(0,1000))
    return user_id

def create_user(user_id, username, email, pwd, joined_from):
    # Automatically generates Username for Google Users based on Google Email
    if user_id == "auto_gen":
        user_id = generate_user_id(username)

    hashed_pwd = hash_user_pwd(pwd)
    user = User.create(user_id, username, email, hashed_pwd, joined_from)
    return user

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

# Compares current time to User Session End Time
def check_session_refresh():
    if session.get("user") and session.get("refresh_time"):
        if datetime.now() > session["refresh_time"]:
            end_user_session()
            return True
    return False
