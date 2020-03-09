import datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout, ConnectionError

from django_project.search_engine.http import resolver

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
                'filters': 'text,packageType,departureRegion,destinationRegion,dateFrom,dateTo,duration,adultsNumber,childrenAge,price,categoryTypes,promotions,food,standard,facilities,grade,transport,tripActivities,tripDifficultyLevels,beachDistance',
                'currency': 'PLN',
                }
            }
    }

def extract_fields(orginal_json, category, provider_name):
    """Take only things that we need"""
    offers_container = orginal_json['data']
    resolver.logger.debug(f"Found {len(offers_container)} record")

    result = []
    for item in offers_container:
        """Country and City is not in any field directly but we can take it
           from the url taken from canonicalDestinationTitle field"""
        soup = BeautifulSoup(item.get('canonicalDestinationTitle', ""), features="html.parser")
        location_info = list(soup.strings)

        try:
            country_name = location_info[0]
        except IndexError:
            resolver.logger.warning("Missing country name! Trying another item.")
            continue

        city_name_list = []
        for i in range(1, len(location_info)):
            if len(location_info[i]) < 4 and '/' in location_info[i]:
                continue
            city_name_list.append(location_info[i].strip(' /'))

        if not city_name_list:
            resolver.logger.warning("Missing city name! Trying another item.")
            continue

        offer = {
            'country': country_name,
            'city': ', '.join(name for name in city_name_list),
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
        }

        hotel_rating = item['ratings']['hotel']
        if hotel_rating:
            offer['hotel_rating'] = hotel_rating

        overall_rating = item['ratings']['overall']
        if overall_rating:
            offer['overall_rating'] = overall_rating

        result.append(offer)

    return result


def get_offers_from_all_pages(url, headers, params, category, provider_name):
    http_resolver = resolver.HttpRequestResolver(url=url, headers=headers)
    num = 1
    result = {
        "offers": []
    }
    while True:
        resolver.logger.debug(f"Parsing page: {num}")
        params['page'] = num
        http_resolver.set_params(params)
        try:
            http_resolver.resolve()
        except resolver.ParameterError as e:
            resolver.logger.exception(e.msg)
            return None
        except Timeout:
            resolver.logger.exception("Timeout when connecting to {provider_name}!")
            return None
        except ConnectionError:
            resolver.logger.exception("Couldn't connect to {provider_name}!")
            return None
        except resolver.ResponseCodeError as e:
            resolver.logger.exception(e.msg)
            continue

        offers_json = resolver.http_resolver()
        parsed_offers = extract_fields(offers_json, category, provider_name)

        if not parsed_offers:
            resolver.logger.info(f"No records for page: {num}. Stopping {provider_name} provider.")
            break
        else:
            result['offers'].extend(parsed_offers)
            num += 1

    return result