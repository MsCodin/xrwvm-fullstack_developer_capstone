# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + str(value) + "&"

    # Prevent double slashes
    if backend_url.endswith('/'):
        request_url = backend_url + endpoint.lstrip('/')
    else:
        request_url = backend_url + endpoint

    if params:
        request_url = request_url + "?" + params

    print("GET from", request_url)

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    # Prevent double slashes
    if sentiment_analyzer_url.endswith('/'):
        request_url = sentiment_analyzer_url + "analyze/" + text
    else:
        request_url = sentiment_analyzer_url + "/analyze/" + text

    print("GET from", request_url)

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None


def post_review(data_dict):
    # Prevent double slashes
    if backend_url.endswith('/'):
        request_url = backend_url + "insert_review"
    else:
        request_url = backend_url + "/insert_review"

    print("POST to", request_url)

    try:
        response = requests.post(request_url, json=data_dict)
        print(response.status_code)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None
