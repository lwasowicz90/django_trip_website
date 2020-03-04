import datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout, ConnectionError

from django_project.search_engine import http

def get_http_request_info():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    return {
        'base_url': 'https://www.itaka.pl/sipl/data/category_ph/search',
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
            'all-inclusive': (
                ('food', 'allInclusive'),
                ('order', 'popular'),
                ),
            'last-minute': (
                ('promo', 'lastMinute'),
                ('order', 'priceAsc'),
                ('filters', ',departureDate'),
                ),
            'common': {
                'view': 'offerList',
                'language': 'pl',
                'package-type': 'wczasy',
                'adults': '2',
                'date-from': today,
                'total-price': '0',
                'transport': 'bus,flight',
                'userId': '5a07c37020f6f23385975533eaa36c9a',
                'page': '1',
                'filters': 'text,packageType,departureRegion,destinationRegion,dateFrom,dateTo,duration,adultsNumber,childrenAge,price,categoryTypes,promotions,food,standard,facilities,grade,transport,tripActivities,tripDifficultyLevels,beachDistance',
                'currency': 'PLN',
                }
            }
    }


class MandatoryFieldError(AttributeError):
    def __init__(self, msg):
        self.msg = msg


def extract_fields(orginal_json, category, provider_name):
    """Take only things that we need"""
    offers_container = orginal_json['data']
    http.logger.debug(f"Found {len(offers_container)} record")

    result = []
    for item in offers_container:
        offer = {
            'id': item['offerId'],
            'category': category,
            'provider': provider_name,
            'price': item['price'],
            'dateFrom': item['dateFrom'],
            'dateTo': item['dateTo'],
            'duration': item['duration'],
            'url': item['url'],
            'img_url': item['photos']['gallery'][0],
            'hotel': item['title'],
            'reviews_cnt': item['reviewsCount'],
            'transport': item['transport'],
            'departureFromCity': item['departure']['from']['city'],
            'departureFromAirPort': item['departure']['from']['airportName'],
        }

        hotel_rating = item['ratings']['hotel']
        if hotel_rating:
            offer['stars'] = hotel_rating/10

        overall_rating = item['ratings']['overall']
        if overall_rating:
            offer['overall'] = overall_rating/10

        """Country and City is not in any field directly but we can take it from some urls"""
        soup = BeautifulSoup(item.get('canonicalDestinationTitle', ""), features="html.parser")

        country_tag = soup.find('a')
        if not country_tag:
            raise MandatoryFieldError("Missing country name!")

        city_tag = country_tag.find_next()
        if not city_tag:
            raise MandatoryFieldError("Missing country name!")

        offer['country'] = country_tag.contents
        offer['city'] = city_tag.contents
        result.append(offer)

    return result


def get_offers_from_all_pages(url, headers, params, category, provider_name):
    resolver = http.RequestResolver(url=url, headers=headers)
    num = 1
    result = []
    while True:
        http.logger.debug(f"Parsing page: {num}")
        params['page'] = num
        resolver.set_params(params)
        try:
            resolver.resolve()
        except http.ParameterError as e:
            http.logger.exception(e.msg)
            return None
        except Timeout:
            http.logger.exception("Timeout when connecting to {provider_name}!")
            return None
        except ConnectionError:
            http.logger.exception("Couldn't connect to {provider_name}!")
            return None
        except http.ResponseCodeError as e:
            http.logger.exception(e.msg)
            continue

        offers_json = resolver.get_json()
        try:
            parsed_offers = extract_fields(offers_json, category, provider_name)
        except MandatoryFieldError as e:
            http.logger.error(e.msg)
            continue

        if not parsed_offers:
            http.logger.info(f"No records for page: {num}. Stopping {provider_name} provider.")
            break
        else:
            result.append(parsed_offers)
            num += 1

    return result
