import unittest
from unittest.mock import patch
from django_project.search_engine.query.provider.itaka.ItakaProvider import ItakaProvider
from django_project.search_engine.query.provider.itaka.utils import get_http_request_info


class TestItakaProvider(unittest.TestCase):
    def setUp(self):
        self.uut = ItakaProvider()
        self.expected_http_request_info = get_http_request_info()
        self.expected_provider_name = "Itaka"

    @patch('django_project.search_engine.query.provider.itaka.utils.get_offers_from_all_pages')
    def test_get(self, get_offers_mock):
        dummy_return_value = {"label": "value"}
        get_offers_mock.return_value = dummy_return_value

        result = self.uut.get()
        get_offers_mock.assert_called_once_with(
            url=self.expected_http_request_info['base_url'],
            headers=self.expected_http_request_info['headers'],
            params=self.expected_http_request_info['params'],
            provider_name=self.expected_provider_name
        )
        self.assertEqual(result, dummy_return_value)
