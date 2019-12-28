import sys
sys.path.append("models")

import SearchValidator

def get_validator(term, location):
    return SearchValidator.get(term, location)

def create_validator(term, location, csrf):
    return SearchValidator.create(term, location, csrf)

def delete_validator(term, location):
    SearchValidator.delete(term, location)

def validate_token(term, location, csrf):
    return SearchValidator.validate_csrf(term, location, csrf)
