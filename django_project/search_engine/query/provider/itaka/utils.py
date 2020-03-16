import datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout, ConnectionError

from django_project.search_engine.http import resolver

def get_http_request_info():
    today = datetime.datetime.today()
    start_day = today.strftime('%Y-%m-%d')
    end_day = (today + datetime.timedelta(days=210)).strftime('%Y-%m-%d')
    return {
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
            'date-from': start_day,
            'date-to': end_day,
            'order': 'popular',
            'total-price': '0',
            'transport': 'bus,flight',
            'filters': 'text,packageType,departureRegion,destinationRegion,dateFrom,dateTo,duration,adultsNumber,childrenAge,price,categoryTypes,promotions,food,standard,facilities,grade,transport,tripActivities,tripDifficultyLevels,beachDistance',
            'currency': 'PLN',
        }
    }

def extract_fields(orginal_json, provider_name):
    """Take only things that we need"""
    offers_container = orginal_json['data']

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
            """Ignore not relevant strings like ' / ' etc. """
            if len(location_info[i]) < 4 and '/' in location_info[i]:
                continue
            city_name_list.append(location_info[i].strip(' /'))

        if not city_name_list:
            resolver.logger.warning("Missing city name!")

        offer = {
            'provider': provider_name,
            'country': country_name,
            'city': ', '.join(name for name in city_name_list),
            'meal': item['meal'],
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

    resolver.logger.info(f"[{provider_name}] Found {len(result)}/{len(offers_container)} correct records on page.")
    return result


def get_offers_from_all_pages(url, headers, params, provider_name):
    http_resolver = resolver.HttpRequestResolver(url=url, headers=headers)
    num = 1
    current_tries = 0
    result = {
        "offers": []
    }
    while True:
        resolver.logger.debug(f"Parsing page: {num} of {provider_name} provider.")
        params['page'] = num
        http_resolver.set_params(params)
        try:
            offers_json = http_resolver.resolve()
        except resolver.ParameterError as e:
            resolver.logger.exception(e.description())
            return result
        except Timeout:
            resolver.logger.exception("Timeout when connecting to {provider_name} provider!")
            return result
        except ConnectionError:
            resolver.logger.exception("Couldn't connect to {provider_name} provider!")
            return result
        except resolver.ResponseCodeError as e:
            resolver.logger.exception(e.description())
            return result

        parsed_offers = extract_fields(offers_json, provider_name)
        if not parsed_offers:
            resolver.logger.info(f"No records for page: {num}. Stopping {provider_name} provider.")
            break
        else:
            result['offers'].extend(parsed_offers)
            num += 1

    resolver.logger.info(f"Found {len(result['offers'])} offers for {provider_name} provider.")
    return result
