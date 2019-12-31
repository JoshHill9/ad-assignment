import sys
sys.path.append("models")

import SearchValidator

# SearchValidatorController used by web-fe.py and search-be.py
# This allows each Service to securely communicate with each other and prevent malicious
# tasks from being submitted to the search-be.py taskqueue.

def get_validator(term, location):
    return SearchValidator.get(term, location)

def create_validator(term, location, csrf):
    return SearchValidator.create(term, location, csrf)

def delete_validator(term, location):
    SearchValidator.delete(term, location)

def validate_token(term, location, csrf):
    return SearchValidator.validate_csrf(term, location, csrf)
