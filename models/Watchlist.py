from google.appengine.api import ndb

import User

class Watchlist(ndb.Model):
    user = ndb.KeyPropety(kind=User)
    watchlist = ndb.StringProperty(repeated=True) #Essentially a String Array (Querying??)
