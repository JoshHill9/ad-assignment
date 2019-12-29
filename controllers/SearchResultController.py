import sys
sys.path.append("models")

from google.appengine.api import modules
import requests, json, ast
import SearchResult

# Find Search Result in Datastore by Entity Key
def get_search_result(term, location):
    return SearchResult.get(term, location)

# Create new Search Result in Datastore
def create_search_result(term, location, result):
    return SearchResult.create(term, location, result)

# Returns 'Expired' if SearchResult has been stored for more than 1 day.
# Returns None if SearchResult is < 1 day old
def check_result_expiry(term, location):
    return SearchResult.is_expired(term, location)

# Deletes Search Result by Key. Key is formed from the 'term' and 'location'
def delete_search_result(term, location):
    SearchResult.delete(term, location)

def format_saved_result(result):
    return ast.literal_eval(result)

# Sends POST request to task-be module with search result data
def queue_search_task(params = {}):
    if params:
        module_url = "http://" + modules.get_hostname(module="task-be") + "/create_task"
        response = requests.post(module_url, data=params)

# Perform Utelly API search
def perform_search(search_term, search_location):
    # Formats Request for Utelly API
    api_url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
    query = {"term": search_term, "country": search_location}
    headers = {
        'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
        'x-rapidapi-key': "18bd841df1mshdd5f213b28bbd71p1611ddjsn225dc187fd4d"
    }
    response = requests.request("GET", api_url, headers=headers, params=query)
    # Retrieves API response
    api_response = json.loads(response.text)
    # Formats sources with no URL into a presentable string.
    if "results" in api_response:
        for result in api_response["results"]:
            if "name" in result:
                if "locations" in result:
                    non_url_locations = ""
                    for location in result["locations"]:
                        if not location["url"]:
                            non_url_locations += location["display_name"] + ", "
                    str_length = len(non_url_locations)
                    if str_length > 0:
                        non_url_locations = non_url_locations[0:str_length-2] + "."
                        result["non_url_locations"] = non_url_locations
    return api_response
