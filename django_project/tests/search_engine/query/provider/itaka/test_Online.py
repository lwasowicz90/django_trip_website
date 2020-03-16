import unittest
from django_project.search_engine.http.resolver import HttpRequestResolver
from django_project.search_engine.query.provider.itaka.utils import get_http_request_info
from django_project.tests.search_engine.query.provider.online_test_cfg import Disabled

"""This test must be run from time to time, to make sure that provider logic is not changed"""
class test_Online(unittest.TestCase):
    @unittest.skipIf(Disabled, "Enable to verify itaka provider logic is not broken")
    def test_fetch_single_page(self):
        info = get_http_request_info()
        url = info["base_url"]
        headers = info["headers"]
        params = info["params"]
        params["page"] = 1

        r = HttpRequestResolver(url, headers=headers)
        r.set_params(params)
        result = r.resolve()
        self.assertGreater(len(result["data"]), 1)
