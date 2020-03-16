from django_project.search_engine.exception.ExceptionWithArgument import ExceptionWithArgument
import requests

class ParameterError(ExceptionWithArgument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, name=self.__class__.__name__)


class ResponseCodeError(ExceptionWithArgument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, name=self.__class__.__name__)


class HttpRequestResolver():
    def __init__(self, url, headers, session=None):
        self.__adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.__url = url
        self.__headers = headers
        self.__params = dict()
        self.__session = session or requests.Session()
        self.__session.mount("http-adapter", self.__adapter)

    def resolve(self):
        if len(self.__params) <= 1:
            raise ParameterError(f"Too little parameters set for request to {self.__url}")

        response = self.__session.get(self.__url, params=self.__params, headers=self.__headers)

        if not response.status_code == 200:
            raise ResponseCodeError(f"Incorrect response code: {response.status_code}!")

        return response.json()

    def set_params(self, value):
        self.__params = value

