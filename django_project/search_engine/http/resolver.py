from django_project.search_engine.exception.ExceptionWithArgument import ExceptionWithArgument
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging_handler = logging.StreamHandler()
logging_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging_handler.setFormatter(formatter)
logger.addHandler(logging_handler)


class ParameterError(ExceptionWithArgument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, name=self.__class__.__name__)


class ResponseCodeError(ExceptionWithArgument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, name=self.__class__.__name__)


class HttpRequestResolver():
    def __init__(self, url, headers, session=None):
        self.adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.url = url
        self.headers = headers
        self.params = dict()
        self.session = session or requests.Session()
        self.session.mount("http-adapter", self.adapter)

    def resolve(self):
        if len(self.params) <= 1:
            raise ParameterError(f"Too little parameters set for request to {self.url}")

        response = self.session.get(self.url, params=self.params, headers=self.headers)

        if not response.status_code == 200:
            raise ResponseCodeError(f"Incorrect response code: {response.status_code}!")

        return response.json()

    def set_params(self, value):
        self.params = value

