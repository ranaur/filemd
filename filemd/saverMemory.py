from .metadataerror import *
import abc

debug = False

class SaverMemory(metaclass=abc.ABCMeta):
    version = "0.0".split(".")
    def description(self):
        return ("SaverMemory", self.version[0] + "." + self.version[1], "Caches metadata information in memory")

    def __init__(self):
        if debug: print("SaverMemory.__init__()")
        self.meta = {}

    def load(self, filename, **args):
        if debug: print("SaverMemory.load(" + filename + ")")
        if not filename in list(self.meta.keys()):
            initData = {}
            self.meta[filename] = initData

    def save(self, filename):
        pass

    def clear(self, filename):
        if debug: print("SaverMemory.clear(" + filename + ")")
        del self.meta[filename]

    def setMeta(self, filename, name, value):
        if debug: print("SaverMemory.setMeta(" + filename + ", " + name + ", " + str(value) + ")")
        try:
            self._checkMeta(filename, name)
        except MetadataNoNameError:
            pass

        self.meta[filename][name] = value

    def getMeta(self, filename, name):
        if debug: print("SaverMemory.getMeta(" + filename + ", " + name + ")")
        self._checkMeta(filename, name)

        return self.meta[filename][name]

    def remove(self, filename, name):
        if debug: print("SaverMemory.remove(" + filename + ", " + name + ")")
        try:
            self._checkName(filename, name)

            del self.meta[filename][name]
        except MetadataNoNameError:
            pass

    def unsetTag(self, filename, name, tag):
        if debug: print("SaverMemory.unsetTag(" + filename + ", " + name + ", " + tag + ")")
        self._checkTag(filename, name)

        if tag in self.meta[filename][name]:
            self.meta[filename][name].remove(tag)
            if len(self.meta[filename][name]) == 0:
                self.remove(filename, name)

    def setTag(self, filename, name, tag):
        if debug: print("SaverMemory.setTag(" + filename + ", " + name + ", " + tag + ")")
        try:
            self._checkTag(filename, name)
        except MetadataNoNameError:
            self.meta[filename][name] = []

        if not tag in self.meta[filename][name]:
            self.meta[filename][name].append(tag)

    def hasTag(self, filename, name, tag):
        if debug: print("SaverMemory.hasTag(" + filename + ", " + name + ", " + tag + ")")
        self._checkTag(filename, name)
        return tag in self.meta[filename][name]

    def getTagList(self, filename, name):
        if debug: print("SaverMemory.getTagList(" + filename + ", " + name + ")")
        self._checkTag(filename, name)
        return self.meta[filename][name]

    def list(self, filename):
        return self.meta[filename]

    def _checkMeta(self, filename, name):
        if self._isTag(filename, name):
            raise MetadataNoMetaError

    def _checkTag(self, filename, name):
        if not self._isTag(filename, name):
            raise MetadataNoTagError

    def _isTag(self, filename, name):
        self._checkName(filename, name)
        return isinstance(self.meta[filename][name], list)

    def _checkName(self, filename, name):
        self._checkFilename(filename)

        if not name in list(self.meta[filename].keys()):
            raise MetadataNoNameError

    def _checkFilename(self, filename):
        if not filename in list(self.meta.keys()):
            raise MetadataNoFileError

saver = SaverMemory
