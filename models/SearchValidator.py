from google.appengine.ext import ndb

# Model Class for 'SearchValidator'
# This validates a form CSRF token against a Search Term and Search Location
# If the Search Term and Location do not match the Form CSRF token, then False is returned
# This is eventually used to prevent malicious Task Queue data from being processed (in search-be.py)

class SearchValidator(ndb.Model):
    search_term = ndb.StringProperty()
    search_location = ndb.StringProperty()
    search_csrf = ndb.StringProperty()

def get(term, location):
    key = term + location
    if key:
        validate_key = ndb.Key("SearchValidator", key)
        return validate_key.get()

def create(term, location, csrf):
    key = term + location
    validator = SearchValidator(id=key)
    validator.search_term = term
    validator.search_location = location
    validator.search_csrf = csrf
    try:
        validator.put()
        return True
    except ValueError:
        pass
    return False

def delete(term, location):
    key = term + location
    validator_key = ndb.Key("SearchValidator", key)
    if validator_key:
        validator_key.delete()

def validate_csrf(term, location, csrf):
    validator = get(term, location)
    if validator:
        if validator.search_csrf == csrf:
            return True
    return False
