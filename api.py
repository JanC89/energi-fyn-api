from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from .exceptions import LoginError
import json

class EnergiFyn:
    _url_predix = 'https://webtools3.energifyn.dk/wts'
    _sessionId = None

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def _generateJsonRequest(self, url):
        req = Request(self._url_predix + url)
        req.add_header('Content-Type', 'application/json')
        if self._sessionId is not None:
            req.add_header('Session-Id', self._sessionId)
        return req

    def _getJsonResult(self, url, data = None):
        req = self._generateJsonRequest(url)
        if data is not None:
            return json.loads(urlopen(req, json.dumps(data).encode()).read().decode())
        else:
            return json.loads(urlopen(req).read().decode())

    def login(self):
        data = {
            'username' : self._username,
            'password' : self._password,
            'rememberLogin' : False,
        }
        try:
            response = self._getJsonResult('/mobileLogin', data)
            print(response['result']['sessionId'])
            self._sessionId = response['result']['sessionId']
        except HTTPError as e:
            response = json.loads(e.read().decode())
            # TODO Check if there in fact is JSON to parse
            raise LoginError(response['errorMsg'])
        
    def getOptions(self):
        try:
            response = self._getJsonResult('/mobileItemGroups')
            print(response)
        except HTTPError as e:
            print(e.read())
