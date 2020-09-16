from flask import render_template, redirect, session
from flask import request
import request_verification_api as a
import os
import requests
from flask import Flask
from flask_caching import Cache
import secrets
from jinja2 import Template
import jinja2


class AuthenteqApi:

    def __init__(self):
        pass

    def verification_result(self):
        value = a.request_verification()
        code = request.args.get('code')
        if code:
            results_url = ("https://api.app.authenteq.com/web-idv/verification-result?code={}".format(code) +
                           "&redirectUrl={}".format(REDIRECT_URL))
            auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
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
