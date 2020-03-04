from search_engine.http.resolver import HttpRequestResolver, ParameterError
import unittest
from unittest.mock import Mock, PropertyMock
from unittest.mock import patch

class TestHttpRequestResolver(unittest.TestCase):

    def setUp(self):
        self.url = "http://dummy.url"
        self.headers = "dummy_header"
        self.params = "dummy_prarams"
        self.response_OK = 200
        self.response_NOK = 400
        self.json_data = "dummy_data"
        self.session_mock = Mock()
        self.uut = HttpRequestResolver(url=self.url, headers=self.headers, session=self.session_mock)
        self.session_mock.mount.assert_called_once()

    def test_resolve_succeeded(self):
        response_mock = Mock()
        response_mock.status_code = self.response_OK
        response_mock.json.return_value = self.json_data
        self.session_mock.get.return_value = response_mock

        self.uut.set_params(self.params)

        result_json = self.uut.resolve()
        self.session_mock.get.assert_called_with(self.url, params=self.params, headers=self.headers)
        response_mock.json.assert_called_once()

        self.assertEqual(result_json, self.json_data)

    # def test_resolve_throw_when_params_not_set(self):
    #     self.assertRaisesRegex(ParameterError, '.*', self.uut.resolve)
    #
    # @unittest.expectedFailure
    # def test_response_not_valid_if_requests_get_not_succeeded(self):
    #     response_mock = Mock()
    #     response_mock.status_code = self.response_NOK
    #     mock_requests.get.return_value = response_mock
    #
    #     self.uut.set_params(self.params)
    #
    #     self.uut.resolve()
    #     mock_requests.get.assert_called_with(self.url, params=self.params, headers=self.headers)
    #
    #     self.assertTrue(self.uut.response_is_valid())
    #


if __name__ == '__main__':
    unittest.main()
