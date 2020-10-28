import requests

class AuthenteqAPIClient:

    API_URL = 'https://api.app.authenteq.com'

    def __init__(self, client_id, client_secret, redirect_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

    def request_verification(self):
        request_verification_url = f'{AuthenteqAPIClient.API_URL}/web-idv/verification-url?redirectUrl={self.redirect_url}'
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        response = requests.request('GET', request_verification_url, auth=auth)
        return response.json()

    def verification_result(self, code):
        results_url = f'{AuthenteqAPIClient.API_URL}/web-idv/verification-result?code={code}&redirectUrl={self.redirect_url}'
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        response = requests.request('GET', results_url, auth=auth)
        return response.json()
