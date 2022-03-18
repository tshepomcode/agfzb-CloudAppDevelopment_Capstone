import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    
    # # Write JSON to a file
    # with open('dealer_review.txt', 'w') as json_file:
    #     json.dump(json_data, json_file)

    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    # Call get_request with a URL parameter or with state
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    
    # json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Setup key to be searched in database
            key = 'id'
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            if key in dealer_doc.keys():
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                    full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"],
                                    long=dealer_doc["long"], short_name=dealer_doc["short_name"], st=dealer_doc["st"],
                                    state=dealer_doc["state"], zip=dealer_doc["zip"]
                                    )
                results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, id=dealerId)
    # json_result = get_request(url)
    print(f'======> json_result = {json_result}')
    with open('review.txt', 'w') as json_file:
        json.dump(json_result, json_file)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_data = json_result["body"]["data"]
        dealers = dealer_data['docs']
        # For each dealer object
        for dealer in dealers:
            # Setup key to be searched in database
            key = 'id'
            # Get its content in `doc` object
            dealer_doc = dealer
            if key in dealer_doc.keys():
                # Create a DealerReview object with values in `doc` object
                dealer_review_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"],
                                    purchase=dealer_doc["purchase"], review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"],
                                    car_make=dealer_doc["car_make"], car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"],
                                    sentiment=dealer_doc["sentiment"], id=dealer_doc["id"]
                                    )
                results.append(dealer_review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
