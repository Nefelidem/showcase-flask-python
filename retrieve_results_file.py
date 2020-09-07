from flask import render_template, redirect, session
from flask import request
import request_verification_api as a
from dotenv import load_dotenv
import os
import requests
from flask import Flask
from flask_caching import Cache
import secrets
from flask_session import Session
from jinja2 import Template


# from flask.ext.session import Session


# load_dotenv(dotenv_path='./credentials.env')

app = Flask(__name__)
app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID')
app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)


# session login to store temporarily the access code for results retrieval
secret = secrets.token_urlsafe(32)
app.secret_key = secret

REDIRECT_URL = 'http://127.0.0.1:5000/results'

# Credentials from admin dashboard stored in environmental variable
CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']

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
    if 'errorCode' not in details_response:
        session['response'] = details_response
        session['response'] = session.get('response')
        for key, value in session.items():
            print('{} => {}'.format(key, value))
    else:
        print('Please try again')


    platform = details_response['platform']
    status = details_response['status']
    id_num = details_response['id']
    start_time = details_response['startTime']
    doc_type = details_response['documentData']['documentType']
    doc_number = details_response['documentData']['documentNumber']
    country = details_response['documentData']['issuingCountry']
    first_name = details_response['documentData']['firstName']
    last_name = details_response['documentData']['lastName']
    given_name = details_response['documentData']['givenNames']
    surname = details_response['documentData']['surname']
    dateofbirth = details_response['documentData']['dateOfBirth']



    return render_template("jinja_template.html", plat=platform, stat=status, id=id_num, starttime=start_time,
                           doctype=doc_type, docnumber=doc_number, issueCountry=country, name=first_name,
                           lastname=last_name, given_name=given_name, Surname=surname, bday=dateofbirth)


if __name__ == "__main__":
    app.run(debug=True)
