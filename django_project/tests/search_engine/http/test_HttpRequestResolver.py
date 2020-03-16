from django_project.search_engine.http.resolver import HttpRequestResolver, ParameterError, ResponseCodeError
import unittest
from unittest.mock import Mock, patch

class TestHttpRequestResolver(unittest.TestCase):
    @patch('requests.Session')
    def setUp(self, session_mock):
        self.actual_session_mock = Mock()
        session_mock.return_value = self.actual_session_mock

        self.url = "http://dummy.url"
        self.headers = "dummy_header"
        self.params = "dummy_prarams"
        self.response_OK = 200
        self.response_NOK = 400
        self.json_data = "dummy_data"
        self.uut = HttpRequestResolver(url=self.url, headers=self.headers)
        self.actual_session_mock.mount.assert_called_once()

    def test_resolve_succeeded(self):
        response_mock = Mock()
        response_mock.status_code = self.response_OK
        response_mock.json.return_value = self.json_data
        self.actual_session_mock.get.return_value = response_mock

        self.uut.set_params(self.params)

        result_json = self.uut.resolve()
        self.actual_session_mock.get.assert_called_with(self.url, params=self.params, headers=self.headers)
        response_mock.json.assert_called_once()

        self.assertEqual(result_json, self.json_data)

    def test_resolve_throw_when_params_not_set(self):
        self.assertRaisesRegex(ParameterError, '.*', self.uut.resolve)

    def test_response_not_valid(self):
        response_mock = Mock()
        response_mock.status_code = self.response_NOK
        self.actual_session_mock.get.return_value = response_mock

        self.uut.set_params(self.params)

        self.assertRaisesRegex(ResponseCodeError, '.*', self.uut.resolve)
        self.actual_session_mock.get.assert_called_with(self.url, params=self.params, headers=self.headers)


if __name__ == '__main__':
    unittest.main()
