import abc

class OfferProviderInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'find') and
                callable(subclass.extract_text) or
                NotImplemented)

    @abc.abstractmethod
    def get(self):
        """Get offers list foor givern category"""
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, filters):
        """Get offers list foor givern filters"""
        raise NotImplementedError