from flask import render_template, redirect
from flask import request
import request_verification_api as a
import os
import requests
from flask import Flask
# from api import AuthenteqApi
from jinja2 import Template
import jinja2

app = Flask(__name__)
REDIRECT_URL = 'http://127.0.0.1:5000/results'
request_verification_url = "https://api.app.authenteq.com/web-idv/verification-url?redirectUrl={}".format(REDIRECT_URL)
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

# home page
@app.route('/')
def start():
    return render_template('index.html')


@app.route('/results', methods=["GET"])
def verification_page():
    value = a.request_verification()
    code = request.args.get('code')
    if code:
        results_url = ("https://api.app.authenteq.com/web-idv/verification-result?code={}".format(code) +
                       "&redirectUrl={}".format(REDIRECT_URL))
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        response = requests.request('GET', results_url, auth=auth)
        details_response = response.json()
        print(details_response)
        print(details_response['platform'])
        if 'errorCode' not in details_response:
            return render_template("results_table.html", platform=details_response['platform'],
                                   status=details_response['status'],
                                   id=details_response['id'],
                                   starttime=details_response['startTime'],
                                   doctype=details_response['documentData']['documentType'],
                                   docnumber=details_response['documentData']['documentNumber'],
                                   issueCountry=details_response['documentData']['issuingCountry'],
                                   name=details_response['documentData']['firstName'],
                                   lastname=details_response['documentData']['lastName'],
                                   given_name=details_response['documentData']['givenNames'],
                                   Surname=details_response['documentData']['surname'],
                                   birthday=details_response['documentData']['dateOfBirth'])
        elif 'errorCode' in details_response:
            print('details_response')
    else:
        return redirect(value)


if __name__ == "__main__":
    app.run(debug=True)
