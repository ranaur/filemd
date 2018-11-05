import yaml
import time
import os
from .saverMemory import SaverMemory
from .metadataerror import *

debug = False

class SaverYAML(SaverMemory):
    version = "0.0".split(".")
    def description(self):
        return ("SaverYAML", self.version[0] + "." + self.version[1], "Stores metadata information in YAML remora file")

    def __init__(self):
        if debug: print("SaverYAML.__init__()")
        super(SaverYAML, self).__init__()

    def load(self, filename):
        if debug: print("SaverYAML.load(self, " + filename + ")")
        super(SaverYAML, self).load(filename)
        try:
            data = open(self._remoraFile(filename), 'r')
        except IOError:
            return

        header = data.readline().rstrip().split(" ", 6)
        if len(header) != 6:
            raise MetadataInvalidFormatError

        if header[0] != "#" or header[1] != "metadata" or header[2] != "YAML":
            raise MetadataInvalidFormatError

        version = header[3].split(".")
        if version[0] != self.version[0] or int(version[1]) > int(self.version[1]):
            raise MetadataInvalidVersionError

        self.timestamp = int(header[4])

        self.headerfile = header[5]
        if self.headerfile != os.path.basename(filename):
            raise MetadataWrongFileFormat

        self.meta[filename] = yaml.load(data)
        if debug: print("LOAD OK")
        if debug: print(self.meta[filename])

    def save(self, filename):
        if debug: print("SaverYAML.save(" + filename + ")")

        if filename in self.meta:
            with open(self._remoraFile(filename), 'w') as outfile:
                header = "# metadata YAML %s.%s %d %s\n" % (self.version[0], self.version[1], time.time(), os.path.basename(filename))
                outfile.write(header)

                outfile.write(yaml.dump(self.meta[filename], default_flow_style=False))

    def clear(self, filename):
        if debug: print("SaverYAML.clear(" + filename + ")")
        try:
            os.remove(self._remoraFile(filename))
        except:
            pass
        super(SaverYAML, self).clear(filename)

    def _remoraFile(self, filename):
        return filename + ".metadata"

saver = SaverYAML
