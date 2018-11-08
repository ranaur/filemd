from .driver import Driver

import datetime

import yaml
import time
import os

from ..metadataerror import *
from ..metadata import MetadataList, Metadata, Tag
from util import name2groupname

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

        res = MetadataList()
        res._driver = self.name()
        if not os.path.isfile(self._remoraFile(identity.file)):
           return res

        with open(self._remoraFile(identity.file), 'r') as data_file:
            header = data_file.readline().rstrip().split(" ", 6)
            data = yaml.load(data_file)

        if len(header) != 6:
            raise MetadataInvalidFormatError

        if header[0] != "#" or header[1] != "metadata" or header[2] != "YAML":
            raise MetadataInvalidFormatError

        res._version = header[3].split(".")
        if res._version[0] != self.version[0] or int(res._version[1]) > int(self.version[1]):
            raise MetadataInvalidVersionError

        res._timestamp = int(header[4])
        res._headerfile = header[5]
        if res._headerfile != os.path.basename(identity.file):
            raise MetadataWrongFileFormat

    
        if data is not None and "metadata" in data and type(data["metadata"]) is dict:
            for md in data["metadata"].keys():
                group, name = name2groupname(md)
                #value, timestamp = data["metadata"][md].rsplit("#",1)
                #value = value.rstrip()
                #timestamp = datetime.datetime.strptime(timestamp.lstrip(), "%Y-%m-%d %H:%M:%S %f")
                timestamp = datetime.datetime.utcfromtimestamp(res._timestamp)
                if type(data["metadata"][md]) is list:
                    for tag in data["metadata"][md]:
                        res.set_tag(group, name, Tag(tag, timestamp=timestamp))
                else:
                    res.set(Metadata(group, name, data["metadata"][md], timestamp))
        if debug: print("LOAD OK")
        return res

    def save(self, identity, metadatalist):
        if debug: print("DriverRemoraYAML.save(" + identity.file + ")")

        with open(self._remoraFile(identity.file), 'w') as outfile:
            header = "# metadata YAML %s.%s %d %s\n" % (self.version[0], self.version[1], time.time(), os.path.basename(identity.file))
            outfile.write(header)

            data = {}
            identity_dict = {}
            if identity.file is not None:
                identity_dict["file"] = identity.file 
            if identity.md5 is not None:
                identity_dict["md5"] = identity.md5 
            if identity.size is not None:
                identity_dict["size"] = identity.size
            if identity.mime is not None:
                identity_dict["mime"] = identity.mime
            if identity.fullpath is not None:
                identity_dict["fullpath"] = identity.fullpath
            if identity.atime is not None:
                identity_dict["atime"] = identity.atime
            if identity.ctime is not None:
                identity_dict["ctime"] = identity.ctime
            if identity.mtime is not None:
                identity_dict["mtime"] = identity.mtime 
            data["identity"] = identity_dict
            data["metadata"] = {}
            for md in metadatalist.metadatas_raw():
                #data["metadata"][md.group + "." + md.name] = md.value + ' # ' + datetime.datetime.strftime(md.timestamp, "%Y-%m-%d %H:%M:%S %f")
                if type(md.value) is dict: # tag
                    tags = list()
                    for tag in md.value:
                        tags.append(md.value[tag].value)
                    data["metadata"][md.group + "." + md.name] = tags
                else:
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

driver_class = DriverRemoraYAML
