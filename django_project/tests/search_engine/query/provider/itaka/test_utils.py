from django_project.search_engine.query.provider.itaka import utils
import unittest
from unittest.mock import Mock, MagicMock
from unittest.mock import patch
import json
import pathlib
import os


class TestUtils_get_http_request_info(unittest.TestCase):
    def setUp(self):
        self.uut = utils.get_http_request_info
        self.dummy_start_date = '2020-09-22'
        self.dummy_end_date = '2020-10-22'
        self.expected_result = \
            {
                'base_url': 'https://www.itaka.pl/sipl/data/search-results/search',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'DNT': '1',
                    'Connection': 'keep-alive-',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'TE': 'Trailers',
                },
                'params': {
                    'view': 'offerList',
                    'language': 'pl',
                    'adults': '2',
                    'date-from': self.dummy_start_date,
                    'date-to': self.dummy_end_date,
                    'order': 'popular',
                    'total-price': '0',
                    'transport': 'bus,flight',
                    'filters': 'text,packageType,departureRegion,destinationRegion,dateFrom,dateTo,duration,adultsNumber,childrenAge,price,categoryTypes,promotions,food,standard,facilities,grade,transport,tripActivities,tripDifficultyLevels,beachDistance',
                    'currency': 'PLN',
                }
            }

    @patch('django_project.search_engine.query.provider.itaka.utils.datetime')
    def test_get_http_request_info(self, mock_datetime):
        add_result_mock = Mock()
        add_result_mock.strftime.return_value = self.dummy_end_date

        strftime_mock_1 = MagicMock()
        strftime_mock_1.__add__.return_value = add_result_mock
        strftime_mock_1.strftime.return_value = self.dummy_start_date
        mock_datetime.datetime.today.return_value = strftime_mock_1

        strftime_mock_2 = Mock()
        mock_datetime.timedelta.return_value = strftime_mock_2

        result = self.uut()
        mock_datetime.datetime.today.assert_called_once()
        strftime_mock_1.strftime.assert_called_once_with('%Y-%m-%d')
        mock_datetime.timedelta.assert_called_once_with(days=210)
        add_result_mock.strftime.assert_called_once_with('%Y-%m-%d')

        self.assertEqual(result, self.expected_result)


class TestUtils_extract_fields(unittest.TestCase):
    def setUp(self):
        self.uut = utils.extract_fields

    def get_expected_offers_list(self, expected_json_filepath):
        with open(expected_json_filepath) as f:
            return json.load(f)['offers']

    def test_parse_two_records_succeeded(self):
        dir_path = pathlib.Path(__file__).parent.absolute()
        path = os.path.join(dir_path, "json_data/two_records_expected.json")
        expected_offers = self.get_expected_offers_list(path)
        dummy_provider = expected_offers[0]['provider']
        with open(os.path.join(dir_path, "json_data/two_records.json")) as f:
            loaded_json = json.load(f)
            result_list = self.uut(loaded_json, dummy_provider)
            self.assertEqual(result_list, expected_offers)

    def test_whole_page_succeeded(self):
        expected_offers_number = 25
        dir_path = pathlib.Path(__file__).parent.absolute()
        path = os.path.join(dir_path, "json_data/single_page_records.json")

        with open(path) as f:
            loaded_json = json.load(f)
            result_list = self.uut(loaded_json, 'dummy_provider')
            expected_offers_number = len(loaded_json['data'])
            self.assertEqual(expected_offers_number, 25)
            self.assertEqual(expected_offers_number, len(result_list))

            input_data = loaded_json['data']
            for i in range(expected_offers_number):
                self.assertTrue(result_list[i]['country'])
                self.assertTrue(result_list[i]['city'])
                self.assertEqual(input_data[i]['meal'], result_list[i]['meal'])
                self.assertEqual(input_data[i]['price'], result_list[i]['price'])
                self.assertEqual(input_data[i]['dateFrom'], result_list[i]['dateFrom'])
                self.assertEqual(input_data[i]['dateTo'], result_list[i]['dateTo'])
                self.assertEqual(input_data[i]['duration'], result_list[i]['duration'])
                self.assertEqual(input_data[i]['url'], result_list[i]['url'])
                self.assertEqual(input_data[i]['photos']['gallery'][0], result_list[i]['img_url'])
                self.assertEqual(input_data[i]['title'], result_list[i]['hotel'])
                self.assertEqual(input_data[i]['reviewsCount'], result_list[i]['reviews_cnt'])
                self.assertEqual(input_data[i]['transport'], result_list[i]['transport'])
                self.assertEqual(input_data[i]['departure']['from']['city'], result_list[i]['departureFromCity'])
                if input_data[i]['ratings']['hotel']:
                    self.assertEqual(input_data[i]['ratings']['hotel'], result_list[i]['hotel_rating'])
                if input_data[i]['ratings']['overall']:
                    self.assertEqual(input_data[i]['ratings']['overall'], result_list[i]['overall_rating'])


if __name__ == '__main__':
    unittest.main()