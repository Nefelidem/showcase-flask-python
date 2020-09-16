import requests
import os

REDIRECT_URL = 'http://127.0.0.1:5000/results'
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

request_verification_url = "https://api.app.authenteq.com/web-idv/verification-url?redirectUrl={}".format(REDIRECT_URL)

if (CLIENT_ID or CLIENT_SECRET) is None:
    print("Create two environmental variables for client id and client secret (instructions in README) "
          "with the values obtained on"
          "the Customer Dashboard (https://customer-dashboard.app.authenteq.com/)")


def request_verification():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.request('GET', request_verification_url, auth=auth)
    x = response.json()
    return list(x.items())[0][1]
