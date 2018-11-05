import os
import abc

class MetadataSaver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def description(self):
        pass

    @abc.abstractmethod
    def load(self, filename): # reads the metadata reference
        pass

    @abc.abstractmethod
    def save(self, filename): # writes the metadata reference
        pass

    @abc.abstractmethod
    def clear(self, filename): # destroy any metadata reference to the file
        pass

    @abc.abstractmethod
    def setMeta(self, filename, name, value): # set a metadata
        pass

    @abc.abstractmethod
    def getMeta(self, filename, name): # gets the metadata value
        pass

    @abc.abstractmethod
    def remove(self, filename, name): # removes a metadata
        pass

    @abc.abstractmethod
    def unsetTag(self, filename, name, tag): # unset a tag
        pass

    @abc.abstractmethod
    def setTag(self, filename, name, tag): # set a tag
        pass

    @abc.abstractmethod
    def hasTag(self, filename, name, tag): # returns true if tag is defined
        pass

    @abc.abstractmethod
    def getTagList(self, filename, name): # returns a list with the tags
        pass

    @abc.abstractmethod
    def list(self, filename): # returns a list of all metadata
        pass

import importlib
here = os.path.dirname(__file__)
__all__ = []
loaded_savers = []
#for fn in os.listdir(here):
#    if fn.startswith("saver") and fn.endswith(".py") and fn != "savers.py":
#        modname = fn[:-3]
#        mod = importlib.import_module("." + modname, __package__)
#        __all__.append(modname)
#        loaded_savers.append(mod.saver())
from .saverYAML import saver
loaded_savers.append(saver())
from .saverMemory import saver
loaded_savers.append(saver())
