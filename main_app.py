from flask import (
    render_template,
    redirect,
    session,
    Flask,
    request
)
import request_verification_api as a
import os
import requests
import secrets
from jinja2 import Template
import jinja2
from flask import request
from flask import Flask
from jinja2 import Template

app = Flask(__name__)


class AuthenteqApi:

    def __init__(self, redirect_url, request_verification_url, client_id, client_secret):
        self.redirect_url = redirect_url
        self.request_verification_url = request_verification_url
        self.client_id = client_id
        self.client_secret = client_secret

    def request_verification(self):
        request_verification_url = AuthenteqApi(
            "https://api.app.authenteq.com/web-idv/verification-url?redirectUrl=http://127.0.0.1:5000/results")
        client_id = AuthenteqApi(os.environ.get('CLIENT_ID'))
        client_secret = AuthenteqApi(os.environ.get('CLIENT_SECRET'))
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        response = requests.request('GET', request_verification_url, auth=auth)
        x = response.json()
        return list(x.items())[0][1]

    def verification_result(self, client_id, client_secret, redirect_url):
        value = a.request_verification()
        code = request.args.get('code')
        if code:
            results_url = ("https://api.app.authenteq.com/web-idv/verification-result?code={}".format(code) +
                           "&redirectUrl={}".format(redirect_url))
            auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
            response = requests.request('GET', results_url, auth=auth)
            details_response = response.json()
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


# home page
@app.route('/')
def start():
    return render_template('index.html')


@app.route('/results', methods=["GET"])
def verification_page():
    verification = AuthenteqApi('http://127.0.0.1:5000/results',
                                "https://api.app.authenteq.com/web-idv/verification-url?redirectUrl=http://127.0.0.1:5000/results",
                                os.environ.get('CLIENT_ID'), os.environ.get('CLIENT_SECRET'))
    return verification.verification_result(os.environ.get('CLIENT_ID'), os.environ.get('CLIENT_SECRET'),
                                            'http://127.0.0.1:5000/results')


if __name__ == "__main__":
    app.run(debug=True)
