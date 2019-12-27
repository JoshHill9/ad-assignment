from google.appengine.ext import ndb
from flask import redirect

class User(ndb.Model):
    user_id = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    join_date = ndb.DateProperty(auto_now_add=True)
    joined_from = ndb.StringProperty()

def find_by_id(user_id=None):
    userKey = ndb.Key("User", user_id)
    return userKey.get()

def find_user_by_name(username=None):
    query = User.query().filter(User.username == username)
    return query.get()

def find_user_by_email(email=None):
    query = User.query().filter(User.email == email)
    return query.get()

def init_user_entity_key(user_id=None):
    if user_id:
        user = User(id=user_id)
        return user
    return None
