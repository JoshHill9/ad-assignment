from google.appengine.ext import ndb
from datetime import datetime, timedelta

class SearchResult(ndb.Model):
    search_term = ndb.StringProperty()
    search_location = ndb.StringProperty()
    search_result = ndb.TextProperty()
    result_expiry = ndb.DateTimeProperty()
    search_date = ndb.DateTimeProperty(auto_now_add=True)

def get(term, location):
    key = term + location
    search_result_key = ndb.Key("SearchResult", key)
    return search_result_key.get()

def delete(term, location):
    key = term + location
    search_result = ndb.Key("SearchResult", key)
    if search_result:
        return search_result.delete()

def is_expired(term, location):
    search_result = get(term, location)
    if search_result:
        if datetime.now() >= search_result.result_expiry:
            return "Expired"
    return None

def create(term, location, result):
    key = term + location
    search_result = SearchResult(id=key)
    search_result.search_term = term
    search_result.search_location = location
    search_result.search_result = result
    search_result.result_expiry = datetime.now() + timedelta(days=1)
    try:
        search_result.put()
        return True
    except ValueError:
        pass
    return False
