from google.oauth2 import id_token
from google.auth.transport import requests

import UserController

def verify_token(provided_token):
    try:
        idinfo = id_token.verify_oauth2_token(provided_token, requests.Request(), "701326295753-m574k0r1pur17bvoj63c5cqtkn72gqj2.apps.googleusercontent.com")

        if idinfo["iss"] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Incorrect Token Issuer")
            return False

        user_id = idinfo["sub"]
        user_email = idinfo["email"]
        user_info = {"user_id": user_id, "user_email": user_email, "user_token": provided_token}
        return user_info
    except ValueError:
        pass
    return False

def check_existing_user(user_id, email, token):
    user = UserController.get_user(email=email)
    if not user:
        username = email[0:email.find("@")]
        if UserController.create_new_user(user_id, username, email, token, "Google"):
            UserController.start_user_session(username, "google_user")
    else:
        UserController.start_user_session(user.username, "google_user")
