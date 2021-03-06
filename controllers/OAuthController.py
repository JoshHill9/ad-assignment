from google.oauth2 import id_token
from google.auth.transport import requests

import UserController

# Controller for authenticating users with OAuth2.0 Google Login
# Google Users are automatically added to the Datastore (see /google_login web-fe.py)
# A username must be auto generated for this, hence the generate_username method
# Google User passwords are not saved or input into the web application

def verify_token(provided_token):
    try:
        idinfo = id_token.verify_oauth2_token(provided_token, requests.Request(), "701326295753-m574k0r1pur17bvoj63c5cqtkn72gqj2.apps.googleusercontent.com")

        if idinfo["iss"] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Incorrect Token Issuer")
            return False

        user_id = idinfo["sub"]
        user_email = idinfo["email"]
        user_info = {"user_email": user_email, "user_token": provided_token, "user_id": user_id}
        return user_info
    except ValueError:
        pass
    return False

def generate_username(email):
    username = email[0:email.find("@")]
    return username

# Looks up User in Datastore and automatically creates account if User is not found
# Starts the User Session for new/existing User
def check_existing_user(email, token):
    user = UserController.get_user(email=email)
    if user:
        return {"username": user.username, "existing_user": True}
    return {"username": generate_username(email), "existing_user": False}
