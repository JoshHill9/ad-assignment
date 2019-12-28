from google.appengine.ext import ndb
from flask import redirect

class User(ndb.Model):
    user_id = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    join_date = ndb.DateProperty(auto_now_add=True)
    joined_from = ndb.StringProperty()

def get_by_id(user_id):
    user_key = ndb.Key("User", user_id)
    return user_key.get()

def get_by_username(username):
    query = User.query().filter(User.username == username)
    return query.get()

def get_by_email(email):
    query = User.query().filter(User.email == email)
    return query.get()

# Returns User Entity initialised with the Entity Key set to the User ID
def create(user_id, username, email, pwd, joined_from):
    if user_id:
        user = User(id=user_id)
        user.user_id = user_id
        user.username = username
        user.email = email
        user.password = pwd
        user.joined_from = joined_from
        try:
            user.put()
            return True
        except ValuError:
            pass
        return False
