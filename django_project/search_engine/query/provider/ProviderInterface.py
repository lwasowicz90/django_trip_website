import abc


class ProviderInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get') and
                callable(subclass.load_data_source) or
                NotImplemented)

    @abc.abstractmethod
    def get(self):
        """Get offers list foor givern category"""
        raise NotImplementedError
