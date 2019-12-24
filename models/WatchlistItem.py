from google.appengine.ext import ndb

# Omitting Entity Key Name creation for this Kind of Entity. Since each User will be able to have multiple Watchlist Items
# Meaning we cannot accurately retrieve User Watchlist Item's by Key. Instead we must use user_id

class WatchlistItem(ndb.Model):
    user_id = ndb.KeyProperty(kind=User)
    item_name = ndb.StringProperty()
    item_url = ndb.StringProperty()
    provider_name = ndb.StringProperty()
    item_order = ndb.IntegerProperty()

def calculate_order(user_id=None):
        if user_id:
            query = WatchlistItem.query().filter(WatchlistItem.user_id == user_id).order(-WatchlistItem.item_order)
            result = query.get()
            if result:
                return result.item_order + 1
            return 1
        return None
