from flask import Flask, render_template, redirect, session
from flask import request
import request_verification_api as a
from dotenv import load_dotenv
import os
import requests
import time
from flask import Flask
from flask_caching import Cache
import secrets

load_dotenv(dotenv_path='./credentials.env')

app = Flask(__name__)

# session login to store temporarily the access code for results retrieval
secret = secrets.token_urlsafe(32)
app.secret_key = secret

REDIRECT_URL = 'http://127.0.0.1:5000/results'

# Credentials from admin dashboard stored in environmental variable
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

request_verification_url = "https://api.app.authenteq.com/web-idv/verification-url?redirectUrl={}".format(REDIRECT_URL)
nd_redirect_url = 'http://127.0.0.1:5000/details'

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# home page
@app.route('/')
def start():
    return render_template('index.html')


@cache.cached(timeout=50)
@app.route('/results', methods=["GET"])
def verification_page():
    value = a.request_verification()
    code = request.args.get('code')
    string_code = str(code)
    request_value = request.get_data
    string_request = str(request_value)
    print('url with access code', string_request)
    if string_code in string_request:
        print(code)
        session['code'] = string_code
        session['code'] = session.get('code')
        for key, value in session.items():
            print('{} => {}'.format(key, value))

    if code:
        return redirect('/details')
    else:
        return redirect(value)


@app.route('/details', methods=["GET"])
def retrieve_results():
    for key, value in session.items():
        print('{} => {}'.format(key, value))
    results_url = ("https://api.app.authenteq.com/web-idv/verification-result?code={}".format(session['code']) +
                   "&redirectUrl={}".format(REDIRECT_URL))
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.request('GET', results_url, auth=auth)
    details_response = response.json()
    print(details_response['platform'])
    # ['id']['status']['platform']['startTime']['documentData']['dateOfBirth']
    return details_response


if __name__ == "__main__":
    app.run(debug=True)
