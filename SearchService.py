import requests, json

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
    # Reformatting of API response to allow for faster client side processing
    compacted_results = []
    if "results" in api_response:
        for result in api_response["results"]:
            if "name" in result:
                if "locations" in result:
                    url_locations = []
                    non_url_locations = ""
                    for location in result["locations"]:
                        # Filters out results with no valid URL
                        if location["url"]:
                            url_locations = url_locations + [{"url": location["url"], "icon": location["icon"], "display_name": location["display_name"]}]
                        else:
                            non_url_locations += location["display_name"] + ", "
                    # Formats aesthetics for results found with no URL
                    list_length = len(non_url_locations)
                    if list_length > 0:
                        non_url_locations = non_url_locations[0:list_length-2] + "."
                    compacted_results = compacted_results + [{"id": result["id"], "name": result["name"], "picture": result["picture"], "locations": url_locations, "non_url_locations": non_url_locations}]
    return compacted_results
