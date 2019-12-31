from google.appengine.ext import ndb
from flask import redirect

# Model Class for 'User'
# Allows for creation and retrieval of User's from the Datastore
# A password reset functionality is also included.

class User(ndb.Model):
    user_id = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    join_date = ndb.DateTimeProperty(auto_now_add=True)

def get_by_id(user_id):
    user_key = ndb.Key("User", user_id)
    return user_key.get()

def get_by_username(username):
    query = User.query().filter(User.username == username)
    return query.get()

def get_by_email(email):
    query = User.query().filter(User.email == email)
    return query.get()

def reset_pwd(username, new_pwd):
    user = get_by_username(username)
    if user:
        user.password = new_pwd
    try:
        user.put()
        return True
    except ValuError:
        pass
    return False

# Returns User Entity initialised with the Entity Key set to the User ID
def create(user_id, username, email, pwd):
    if user_id:
        user = User(id=user_id)
        user.user_id = user_id
        user.username = username
        user.email = email
        user.password = pwd
        try:
            user.put()
            return True
        except ValuError:
            pass
        return False
