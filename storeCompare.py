# api_caller.py

import requests
from pprint import pprint

def call_api(search_term):
    payload = {
        'source': 'amazon_search',
        'domain': 'com',
        'query': search_term,
        'start_page': 1,
        'pages': 2,
        'parse': True,
        # 'context': [
        #     {'key': 'category_id', 'value': 16391693031}
        #],
    }
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('maxton', 'Cougmgj7Cougmgj7'),
        json=payload,
    )
    return response.json()

def find_lowest_price_item(api_response):
    lowest_price = float('inf')  # Set to infinity initially
    lowest_price_item = None

    # Iterate over the results in the JSON response
    for result in api_response['results']:
        for item in result['content']['results']['amazons_choices'] + result['content']['results']['organic']:
            if 'price' in item and item['price'] != 0:  # Check for price key, removes false 0 prices
                if item['price'] < lowest_price:
                    lowest_price = item['price']
                    lowest_price_item = item
    # Check if any item with a price was found
    if lowest_price_item is not None:
        return lowest_price_item['title'], lowest_price
    else:
        return "No items found with a price", None



if __name__ == "__main__":
    search_term = 'nirvana shirt'
    api_response = call_api(search_term)
    #pprint(api_response)
    item_name, item_price = find_lowest_price_item(api_response)
    print("Lowest price item:", item_name)
    print("Price:", item_price)
