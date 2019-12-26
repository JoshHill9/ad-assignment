from google.appengine.ext import ndb
import User

# Omitting Entity Key Name creation for this Kind of Entity. Since each User will be able to have multiple Watchlist Items
# Meaning we cannot accurately retrieve User Watchlist Item's by Key. Instead we must use user_id

class WatchlistItem(ndb.Model):
    user_id = ndb.KeyProperty(kind=User.User)
    item_name = ndb.StringProperty()
    item_url = ndb.StringProperty()
    provider_name = ndb.StringProperty()
    item_order = ndb.IntegerProperty()

def get_user_watchlist(user_id=None, order=None, max_results=50):
    if user_id:
        if order:
            query = WatchlistItem.query().filter(WatchlistItem.user_id == user_id).order(order)
        query=WatchlistItem.query().filter(WatchlistItem.user_id == user_id)
        return query.fetch(max_results)
    return None

# Grabs the highest item_order value in the users watchlist to calculate next value.
# If no value is found. Initiate watchlist with item_order of 1.
def calculate_order(user_id=None):
        if user_id:
            result = get_user_watchlist(user_id, -WatchlistItem.user_id, 1)
            if result:
                return result.item_order + 1
            return 1
        return None

def create_watchlist_item(user_id, item_name, item_url, provider_name):
    item_order = calculate_order(user_id)
    watchlist_item = WatchlistItem(user_id, item_name, item_url, provider_name, item_order)
    return watchlist_item
