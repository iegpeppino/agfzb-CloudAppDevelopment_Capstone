import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of request library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params= kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))    
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a url parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as Dealers
        dealers = json_result["docs"]
        for dealer in dealers:
            # Create a CarDealer object with values in 'doc' object
            dealer = CarDealer(address= dealer["address"], city = dealer["city"], full_name= dealer["full_name"],
            id = dealer["id"], lat = dealer["lat"], long = dealer["long"], short_name= dealer["short_name"],
            st = dealer["st"], state= dealer["state"], zip= dealer["zip"])
            results.append(dealer)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    dealer_id = kwargs["dealer_id"]
    json_result = get_request(url, dealerId= dealer_id)
    if json_result:
        reviews = json_result["docs"]
        for review in reviews:
            if review["purchase"] == True:
                review = DealerReview(review = review["review"],name= review["name"], dealership= review["dealership"], purchase= review["purchase"],
                purchase_date= review["purchase_date"], car_make= review["car_make"], car_model= review["car_model"],
                car_year= review["car_year"], sentiment = analyze_review_sentiments(review["review"]))
                results.append(review)
            else:
                review = DealerReview(review = review["review"],name= review["name"], dealership= review["dealership"], purchase= review["purchase"],
                purchase_date= '', car_make= 'None', car_model= '',
                car_year= 'None', sentiment = analyze_review_sentiments(review["review"]))
                results.append(review)    
    return results 


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/259ed973-656e-4faa-bc78-171f23fb2572'
    api_key = 'kMi7yosRjwE3agBhxDpAyDqJWRfVutElD7Ty_A33CmUk'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version = "2021-03-25", authenticator = authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text = dealerreview, features = Features(sentiment = SentimentOptions()), language="en").get_result()
    sentiment_label = response["sentiment"]["document"]["label"]
    return sentiment_label