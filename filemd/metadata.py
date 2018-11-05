import abc
import os
from .metadataerror import *

class Metadata(metaclass=abc.ABCMeta):
    def __init__(self, filename, savers, defaultSaver = 0):
        if not os.path.isfile(filename):
            raise os.IOError(2, os.strerror(2), filename)

        #if not os.access(filename, os.R_OK):
        #    raise os.IOError(13, os.strerror(13), filename)

        self.filename = filename

        if not isinstance(savers, list):
            raise TypeError

        self.savers = savers

        for saver in reversed(self.savers):
            saver.load(self.filename)

        # syncs every saver
        #self.save()

        if defaultSaver < 0 or defaultSaver > len(savers) - 1:
            raise IndexError
        self.defaultSaver = defaultSaver
        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.save()
        return True

    def __del__(self):
        #self.save()  -- if you don't use the with syntax, you must save the file
        return True

    def initialize(self):
        pass

    def save(self): # writes the metadata reference
        for saver in self.savers:
            saver.save(self.filename)

    def clear(self): # destroy any metadata reference to the file
        for saver in self.savers:
            saver.clear(self.filename)

    def setMeta(self, name, value = None):
        if value is None:
            self.remove(name)
            return

        if type(value) is list:
            value = ", ".join(value)

        if type(value) is str:
            value = value

        for saver in self.savers:
            saver.setMeta(self.filename, name, value)

    def getMeta(self, name, default = None):
        try:
            return self.savers[self.defaultSaver].getMeta(self.filename, name)
        except MetadataNoNameError:
            if default is None:
                raise MetadataNoNameError

            return default

    def remove(self, name):
        for saver in self.savers:
            saver.remove(self.filename, name)

    def unsetTag(self, name, tag):
        for saver in self.savers:
            saver.unsetTag(self.filename, name, tag)

    def setTag(self, name, tag):
        for saver in self.savers:
            saver.setTag(self.filename, name, tag)

    def hasTag(self, name, tag):
        return self.savers[self.defaultSaver].hasTag(self.filename, name, tag)

    def getTagList(self, name, tag):
        return self.savers[self.defaultSaver].getTagList(self.filename, name, tag)

    def listSavers(self):
        res = []
        for saver in self.savers:
            res.append(saver.description())
        return res

    def list(self):
        return self.savers[self.defaultSaver].list(self.filename)

