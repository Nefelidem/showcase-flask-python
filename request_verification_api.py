import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='./credentials.env')


REDIRECT_URL = 'http://127.0.0.1:5000/results'
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


request_verification_url = "https://api.app.authenteq.com/web-idv/verification-url?redirectUrl={}".format(REDIRECT_URL)

if (CLIENT_ID or CLIENT_SECRET) is None:
    print("Create .env file in the root of the project with CLIENT_ID and CLIENT_SECRET variables. You will find their"
          " values in the Customer Dashboard (https://customer-dashboard.app.authenteq.com/)")


def request_verification():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.request('GET', request_verification_url, auth=auth)
    x = response.json()
    print(list(x.items())[0][1])
    return list(x.items())[0][1]








