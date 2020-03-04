import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ParameterError(AssertionError):
    def __init__(self, msg):
        self.msg = msg


class ResponseCodeError(ValueError):
    def __init__(self, msg):
        self.msg = msg


class HttpRequestResolver():
    def __init__(self, url, headers, session=None):
        self.adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.url = url
        self.headers = headers
        self.params = None
        self.session = session or requests.Session()
        self.session.mount("http-adapter", self.adapter)

    def resolve(self):
        if not self.params:
            raise ParameterError(f"Parameters not set for request to {self.url}")

        response = self.session.get(self.url, params=self.params, headers=self.headers)

        if not response.status_code == 200:
            raise ResponseCodeError(f"Incorrect response code: {response.status_code}!")

        return response.json()

    def set_params(self, value):
        self.params = value

