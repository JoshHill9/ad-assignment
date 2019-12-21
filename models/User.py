from google.appengine.api import users
from google.appengine.ext import ndb
from flask import redirect

class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    join_date = ndb.DateProperty(auto_now_add=True)
    joined_from = ndb.StringProperty()

def findUserByName(username=None):
    userKey = ndb.Key('User', username)
    return userKey.get()

def findUserByEmail(email=None):
    query = User.query().filter(User.email == email)
    return query.get()

def initUserEntityKey(username=None):
    if username:
        user = User(id=username)
        return user
    return None

def getCurrentUser():
    user = users.get_current_user()
    if user:
        return user
    return None

def getUserLoginURL():
    return users.create_login_url('/account')

def getUserLogoutURL():
    return users.create_logout_url('/login')

def loginUser():
    user = users.get_current_user()
    return user

def logoutUser():
    return redirect(getUserLogoutURL)
