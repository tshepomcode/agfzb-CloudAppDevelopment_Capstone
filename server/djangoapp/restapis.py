from pickle import TRUE
from urllib import response
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request(url, **kwargs):
    # api_key = ''
    # review = ''
    review = kwargs.get('dealerreview')
    api_key = kwargs.get('api_key')
    print(kwargs)
    print("GET from {} ".format(url))
    # try:
    #     # Call get method of requests library with URL and parameters
    #     response = requests.get(url, headers={'Content-Type': 'application/json'},
    #                             params=kwargs)
    # except:
    #     # If any error occurs
    #     print("Network exception occurred")
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["language"] = kwargs["language"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('api_key', api_key))
        else:
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


def post_request(url, payload, **kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ". format(status_code))
    json_data = json.loads(response.text)

    return json_data

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
    # print(f'======> json_result = {json_result}')
    # with open('review.txt', 'w') as json_file:
    #     json.dump(json_result, json_file)
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
                sentiment = analyze_review_sentiments(dealer_doc["review"])
                print(sentiment)

                # Create a DealerReview object with values in `doc` object
                dealer_review_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"],
                                                 purchase=dealer_doc["purchase"], review=dealer_doc["review"]
                                                 )
                # if dealer_doc['purchase'] == True:
                #     dealer_review_obj.id = dealer_doc["id"]
                #     dealer_review_obj.puchase_date = dealer_doc["purchase_date"]
                #     dealer_review_obj.car_make = dealer_doc["car_make"]
                #     dealer_review_obj.car_model = dealer_doc["car_model"]
                #     dealer_review_obj.car_year = dealer_doc["car_year"]

                dealer_review_obj.sentiment = sentiment
                results.append(dealer_review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/76981f41-32f6-469d-b016-998f82f81345/v1/analyze'
    api_key = 'HhX42guzXHFX_G8VinROszwYQ1ajlGVfCfn9ywAvS3UI'

    params = dict()
    params['api_key'] = api_key
    params['text'] = dealerreview
    params['version'] = '2021-08-01'
    params['features'] = 'sentiment'
    params['return_analyzed_text'] = True
    params['language'] = 'en'
    response = get_request(url, kwargs=params)

    return response
