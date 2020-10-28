import os
import pycountry

from flask import (
    render_template,
    redirect,
    request,
    Flask,
)

from api import AuthenteqAPIClient


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URL = 'http://127.0.0.1:5000/results'

API_CLIENT = AuthenteqAPIClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

app = Flask(__name__)

SEX = {
  'M': 'Male',
  'F': 'Female',
  'X': 'Unspecified',
}

@app.template_filter()
def sex(value):
    return SEX[value]

DOCUMENT_TYPES = {
  'PP': "Passport",
  'DL': "Driver's License",
  'NID': "National ID Card",
}

@app.template_filter()
def document_type(value):
    return DOCUMENT_TYPES[value]

@app.template_filter()
def data_url(image_object):
    content_type = image_object['contentType']
    content = image_object['content']
    return f'data:{content_type};base64,{content}'

@app.template_filter()
def conuntry(code):
    return pycountry.countries.get(alpha_3=code).name

@app.route('/')
def index():
    API_CLIENT.request_verification()
    api_response = API_CLIENT.request_verification()
    if 'verificationUrl' in api_response:
        verification_url = api_response['verificationUrl']
        return render_template('index.html', verification_url=verification_url)
    elif api_response.get('errorCode') == 'INVALID_REQUEST_PARAMETER':
        message = api_response['errorMessage']
        return render_template('error.html', message=message)


@app.route('/results')
def results():
    code = request.args.get('code')
    if code:
        api_response = API_CLIENT.verification_result(code)
        if api_response.get('errorCode') == 'INVALID_REQUEST_PARAMETER':
            message = api_response['errorMessage']
            return render_template('error.html', message=message)
        return render_template("results.html", document_data=api_response['documentData'])
    else:
        return render_template('error.html', message="The verification has been interrupted.")


if __name__ == "__main__":
    app.run(debug=True)
