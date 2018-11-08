import abc

class Driver:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def description():
        pass

    @abc.abstractmethod
    def load(self, identity): # return a metadataList
        pass

    @abc.abstractmethod
    def save(self, identity, metadatalist):
        pass

    @abc.abstractmethod
    def clear(self, identity):
        pass

