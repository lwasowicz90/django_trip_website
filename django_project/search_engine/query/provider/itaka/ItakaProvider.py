from django_project.search_engine.query.provider.ProviderInterface import ProviderInterface
from django_project.search_engine.query.provider.itaka import utils


class ItakaProvider(ProviderInterface):
    """header and params for http get request"""
    __http_request_info = utils.get_http_request_info()
    __provider_name = "Itaka"

    def get(self):
        """Overrides OfferProviderInterface.get()"""
        return self.__get()

    def __get(self):
        """Gathers all offers"""
        return utils.get_offers_from_all_pages(url=ItakaProvider.__http_request_info['base_url'],
                                               headers=ItakaProvider.__http_request_info['headers'],
                                               params=ItakaProvider.__http_request_info['params'],
                                               provider_name=ItakaProvider.__provider_name)
