from .driver import Driver

import datetime

import yaml
import time
import os

from ..metadataerror import *
from ..metadata import MetadataList, Metadata

debug = False

class DriverRemoraYAML(Driver):
    version = "0.0".split(".")
    def name(self):
        return "DriverRemoraYAML"
        
    def description(self):
        return ("DriverRemoraYAML", self.version[0] + "." + self.version[1], "Stores metadata information in YAML remora file")

    def __init__(self, *args):
        if debug: print("DriverRemoraYAML.__init__()")
        super(Driver, self).__init__()

    def load(self, identity):
        if debug: print("DriverRemoraYAML.load(self, " + identity.file + ")")
        try:
            data = open(self._remoraFile(identity.file), 'r')
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
        if self.headerfile != os.path.basename(identity.file):
            raise MetadataWrongFileFormat

        data = yaml.load(data)

        if debug: print("LOAD OK")
        res = MetadataList()
        for md in data["metadata"].keys():
            group, name = md.split(".", 1)
            #value, timestamp = data["metadata"][md].rsplit("#",1)
            #value = value.rstrip()
            #timestamp = datetime.datetime.strptime(timestamp.lstrip(), "%Y-%m-%d %H:%M:%S %f")
            value = data["metadata"][md]
            timestamp = datetime.datetime.utcfromtimestamp(self.timestamp)
            res.set(Metadata(group, name, value, timestamp))
        return res

    def save(self, identity, metadatalist):
        if debug: print("DriverRemoraYAML.save(" + identity.file + ")")

        with open(self._remoraFile(identity.file), 'w') as outfile:
            header = "# metadata YAML %s.%s %d %s\n" % (self.version[0], self.version[1], time.time(), os.path.basename(identity.file))
            outfile.write(header)

            data = {}
            data["identity"] = {
                "file" : identity.file,
                "md5" : identity.md5,
                "size" : identity.size,
                "mime" : identity.mime,
                "fullpath" : identity.fullpath,
                "atime" : identity.atime,
                "ctime" : identity.ctime,
                "mtime" : identity.mtime,
            }
            data["metadata"] = {}
            for md in metadatalist.metadatas_raw():
                #data["metadata"][md.group + "." + md.name] = md.value + ' # ' + datetime.datetime.strftime(md.timestamp, "%Y-%m-%d %H:%M:%S %f")
                data["metadata"][md.group + "." + md.name] = md.value
            
            outfile.write(yaml.dump(data, default_flow_style=False))

    def clear(self, identity):
        if debug: print("DriverRemoraYAML.clear(" + identity.file + ")")
        try:
            os.remove(self._remoraFile(identity.file))
        except:
            pass

    def _remoraFile(self, filename):
        return filename + ".metadata"

