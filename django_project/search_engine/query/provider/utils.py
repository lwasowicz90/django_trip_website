import datetime
from bs4 import BeautifulSoup

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


def extract_fields(orginal_json, category, provider_name):
    """Take only things that we need"""
    offers_container = orginal_json['data']
    print(f"\t offers: {len(offers_container)}")
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
        if (hotel_rating):
            offer['stars'] = hotel_rating/10

        overall_rating = item['ratings']['overall']
        if (overall_rating):
            offer['overall'] = overall_rating/10

        """Country and City is not in any field directly but we can take it from some urls"""
        # soup = BeautifulSoup(item['canonicalDestinationTitle'], features="html.parser")
        # # needs to handle exeption if out of range:!!!!!!
        # first_tag_with_value = soup.find('a')
        # second_tag_with_value = first_tag_with_value.find_next()
        # offer['country'] = first_tag_with_value.contents
        # offer['city'] = second_tag_with_value.contents
        result.append(offer)

    return result


def get_offers_from_all_pages(url, headers, params, category, provider_name):
    ##handle eceptions!
    resolver = http.RequestResolver(url=url, headers=headers)
    num = 1
    result = []
    while True:
        print(f"parsing page: {num}")
        params['page'] = num
        resolver.set_params(params)
        resolver.resolve()
        #remove is_valid and handle exeption
        if not resolver.is_valid():
            print("Resolver not valid ERROR")
            return None
        offers_json = resolver.get_json()
        parsed_offers = extract_fields(offers_json, category, provider_name)
        if not parsed_offers:
            print("not parsed_offers:")
            break
        else:
            result.append(parsed_offers)
            num += 1

    return result
