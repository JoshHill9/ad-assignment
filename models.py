from google.appengine.api import users

def isUserLoggedIn():
    foundUser = users.get_current_user()
    return {"found": True} if foundUser else {"found": False}
