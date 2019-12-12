from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()
    user = ndb.UserProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()

def isUserLoggedIn():
    foundUser = users.get_current_user()
    if foundUser:
        logout_url = users.create_logout_url('/login')
        user = {'userObj': foundUser, 'logout_url': logout_url, 'logged_in': True}
        return user
    login_url = users.create_login_url('/login')
    userLogin = {'logged_in': False, 'login_url': login_url}
    return userLogin
