import requests

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
    total_price = 0
    count = 0
    imgurl = ""

    # Iterate over the results in the JSON response
    for result in api_response['results']:
        for item in result['content']['results']['amazons_choices'] + result['content']['results']['organic']:
            if 'price' in item and item['price'] != 0:  # Check for price key, removes false 0 prices
                count += 1
                total_price += item['price']
                if item['price'] < lowest_price:
                    lowest_price = item['price']
                    lowest_price_item = item
                    imgurl = item['url_image']

    # Check if any item with a price was found
    if lowest_price_item is not None:
        average_price = round(total_price / count, 2) if count != 0 else 0
        return lowest_price_item['title'], lowest_price, imgurl, average_price, count
    else:
        return "No items found with a price", None, None, None, count


def run_search(search_term):
    api_response = call_api(search_term)
    name, price, imgurl, avg_price, count = find_lowest_price_item(api_response)
    name_text = "Lowest price item: " + name
    price_text = f"Price: ${price}"
    avg_text = f"Average price: ${avg_price}"
    count_text = f"{count} items checked"
    return name_text, price_text, imgurl, avg_text, count_text

