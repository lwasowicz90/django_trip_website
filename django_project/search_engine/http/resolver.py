import requests

class ParameterError(ValueError):
    def __init__(self, arg):
        self.arg = arg


class HttpRequestResolver():

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.params = None
        self.response = None

    def resolve(self):
        if not self.params:
            raise ParameterError(f"Empty params in {self.__class__.__name__}.{self.resolve.__name__}")

        self.response = requests.get(self.url, params=self.params, headers=self.headers)

    def set_params(self, value):
        self.params = value

    def response_is_valid(self):
        return self.response.status_code == 200

    def get_json(self):
        return self.response.json()
