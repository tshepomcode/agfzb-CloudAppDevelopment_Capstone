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
    print(kwargs)
    print(f"POST to {url}")
    print(payload)
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
    print(f'======> json_result = {json_result}')
    print(f'======> type(json_result) = {type(json_result)}')
    # with open('review1.txt', 'w') as json_file:
    #     json.dump(json_result, json_file)
    if json_result:
        # Get the row list in JSON as dealers
        data_keys = json_result['body'].keys()
        print(f"data_keys['body']: {data_keys}")
        if 'data' in json_result['body']:
            the_dealers_data = json_result["body"]["data"]
            dealers = the_dealers_data['docs']
            print(f"the_dealers_data:\n{the_dealers_data}\n")
            print(f"the_dealers_doc:\n{dealers}\n")
        else:
            dealers = json_result["body"]["docs"]
            # this_dealer_doc = json_result["docs"]
            print(f"this_dealer_data:\n{dealers}\n")
            # print(f"this_dealer_doc: \n{this_dealer_doc}\n")

        # dealer_data = json_result["body"]["data"]
        # dealers = dealer_data['docs']
        # For each dealer object
        for dealer in dealers:
            # Setup key to be searched in database
            key = 'id'
            # Get its content in `doc` object
            dealer_doc = dealer
            print(f"dealer: {dealer}")
            if key in dealer_doc.keys():
                
                # print(f'sentiment = {sentiment}')
                
                if dealer_doc['purchase'] == True:
                    dealership = dealer_doc["dealership"]
                    name = dealer_doc["name"]
                    purchase = dealer_doc["purchase"]
                    review = dealer_doc["review"]
                    purchase_date = dealer_doc["purchase_date"]
                    car_make = dealer_doc["car_make"]
                    car_model = dealer_doc["car_model"]
                    car_year = dealer_doc["car_year"]
                    id = dealer_doc["id"]
                    sentiment = analyze_review_sentiments(dealer_doc["review"])
                     # Create a DealerReview object with values in `doc` object
                    dealer_review_obj = DealerReview(dealership=dealership, name=name, purchase=purchase,
                                                 review=review, purchase_date=purchase_date, car_make=car_make,
                                                 car_model=car_model,car_year=car_year, sentiment=sentiment,
                                                 id = id
                                                 )
                elif dealer_doc['purchase'] == False:
                    dealership = dealer_doc["dealership"]
                    name = dealer_doc["name"]
                    purchase = dealer_doc["purchase"]
                    review = dealer_doc["review"]
                    purchase_date = None
                    car_make = None
                    car_model = None
                    car_year = None
                    id = dealer_doc["id"]
                    sentiment = analyze_review_sentiments(dealer_doc["review"])
                     # Create a DealerReview object with values in `doc` object
                    dealer_review_obj = DealerReview(dealership=dealership, name=name, purchase=purchase,
                                                 review=review, purchase_date=purchase_date, car_make=car_make,
                                                 car_model=car_model,car_year=car_year, sentiment=sentiment,
                                                 id = id
                                                 )
                # results.append(dealer_review_obj)


                # Create a DealerReview object with values in `doc` object
                # dealer_review_obj = DealerReview(dealership=dealership, name=name, purchase=purchase,
                #                                  review=review, purchase_date=purchase_date, car_make=car_make,
                #                                  car_model=car_model,car_year=car_year, sentiment=sentiment,
                #                                  id = id
                #                                  )
                # if dealer_doc['purchase'] == True:
                #     dealer_review_obj.id = dealer_doc["id"]
                #     dealer_review_obj.puchase_date = dealer_doc["purchase_date"]
                #     dealer_review_obj.car_make = dealer_doc["car_make"]
                #     dealer_review_obj.car_model = dealer_doc["car_model"]
                #     dealer_review_obj.car_year = dealer_doc["car_year"]

                # dealer_review_obj.sentiment = sentiment
                # print(f'dealer review obj.car_model {dealer_review_obj.car_model}')
                results.append(dealer_review_obj)
            else:
                return {'error' : 'The are no reviews for the dealeship'}

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EntitiesOptions, KeywordsOptions
    from ibm_watson import AssistantV1, ApiException

    # with open('/etc/nlu_api_key.txt') as f:
    #     api_key = f.read().strip()
    
    api_key = 'HhX42guzXHFX_G8VinROszwYQ1ajlGVfCfn9ywAvS3UI'

    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/76981f41-32f6-469d-b016-998f82f81345'

    params = dict()
    params['api_key'] = api_key
    params['text'] = dealerreview
    params['version'] = '2021-08-01'
    params['features'] = 'sentiment'
    params['return_analyzed_text'] = True
    params['language'] = 'en'

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=params['version'],
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(
            sentiment=SentimentOptions(targets=[dealerreview])
            ),
        language='en').get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    # print(json.dumps(response, indent=2))

    # response = get_request(url, kwargs=params)

    return label
