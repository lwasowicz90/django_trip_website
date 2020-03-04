from . import trip_categories
from . import OfferProviderInterface
from . import utils


class ItakaOfferProvider(OfferProviderInterface.OfferProviderInterface):
    """header and params for http get request"""
    http_request_info = utils.get_http_request_info()
    provider_name = "Itaka"

    def __init__(self):
        """This is value for ph in http_request_info.base_url"""
        #self.categories = categories

    def get(self):
        """Overrides OfferProviderInterface.get()"""
        temp_category = 'all-inclusive'
        return self.__get(temp_category)

    def find(self, filters):
        """Overrides OfferProviderInterface.find()"""
        raise NotImplementedError

    def __make_params_dict(self, base_params, unique_params):
        for k,v in unique_params:
            if k in base_params:
                base_params[k] += v
            else:
                base_params[k] = v

    def __get(self, category):
        """Go through the category and gather offers"""
        print(f"calling get with {category}")

        params = ItakaOfferProvider.http_request_info['params']['common']
        unique_params = ItakaOfferProvider.http_request_info['params'][category]
        self.__make_params_dict(params, unique_params)
        url = ItakaOfferProvider.http_request_info['base_url'].replace('category_ph', category)

        return utils.get_offers_from_all_pages(url=url,
                                               headers=ItakaOfferProvider.http_request_info['headers'],
                                               params=params,
                                               category=category,
                                               provider_name=ItakaOfferProvider.provider_name)
