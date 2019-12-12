from google.appengine.api import users

def isUserLoggedIn():
    foundUser = users.get_current_user()
    if not foundUser is None:
        return {"found": true}
    else:
        return {"found": false}