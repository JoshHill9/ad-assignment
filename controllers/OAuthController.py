import sys
sys.path.append("lib")

from google.oauth2 import id_token
from google.auth.transport import requests

def verifyToken(provided_token):
    try:
        idinfo = id_token.verify_oatuh2_token(provided_token, requests.Request(), "701326295753-m574k0r1pur17bvoj63c5cqtkn72gqj2.apps.googleusercontent.com")

        if idinfo["iss"] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Incorrect Token Issuer")
            return False

        user_id = idinfo["sub"]
        return True
    except ValueError:
        pass
    return False
