import datetime

# Types
DETECT = 0
TEXT = 1
NUMBER = 2
DATETIME = 3
DATA = 4
TAG = 5

class MetadataSyncError(Exception):
    pass

class Timestamped:
    def __init__(self, timestamp = None):
        self.timestamp = timestamp

    @property
    def timestamp(self):
        return self.__timestamp
    @timestamp.setter
    def timestamp(self, value = None):
        self.__timestamp = value if value is not None else datetime.datetime.now()
    def touch(self):
        self.timestamp()


class Metadata(Timestamped):
    def __init__(self, var, name = None, value = None, type_ = DETECT, timestamp = None):
        super.__init__(var.timestamp)
        if var is Metadata:
            self.group = var.group
            self.name = var.name
            self.type = var.type
            self.value = var.value
            self.timestamp = var.timestamp
        else:
            self.group = var
            self.name = name
            self.value = var.value
            self.type = type_
            self.timestamp = timestamp

    @property
    def group(self):
        return self.__group
    @group.setter
    def group(self, value):
        self.__group = value
        self.touch()

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value
        self.touch()

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, _value):
        self.__value = _value
        self.touch()

    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, value):
        self.__type = value
        self.touch()


class Tag:
    def __init__(self, var, group = None, type_ = DETECT, timestamp = None):
        if var is Tag:
            self.value = var.value
            self.group = var.group
            self.type = var.type
            self.timestamp = var.timestamp
        else:
            self.value = var
            self.group = group
            self.type = type_
            self.typestamp = timestamp

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, _value):
        self.__value = _value
        self.touch()

    @property
    def group(self):
        return self.__group
    @group.setter
    def group(self, value):
        self.__group = value
        self.touch()

    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, value):
        self.__type = value
        self.touch()

class MetadataList():
    def __init__(self):
        self.groups = {}

    def merge(self, otherlist):
        for ol_md in otherlist.metadatas:
            my_md = self.get(md.group, md.name) 

            if my_md.value != ol_md.value or my_md.type != my_md.type:
                if ol_md.timestamp == my_md.timestamp:
                    raise MetadataSyncError
                self.set(ol_md)

    def set(self, var, name = None, value = None, _type = DETECT):
        if var is list: # List of metadatas
            if len(var) == 0:
                return

            if var[0] is Metadata:
                for v in var:
                    self.set(v)
                return

            if var[0] is List:
                for v in var:
                    group = v[0]
                    name = v[1]
                    value = v[2]
                    _type = v[3] if len(v) == 3 else DETECT
                    self.set(Metadata(group, name, value, _type))
                return


        if var is str and name is str and value is not None:
            self.set(Metadata(var, name, value, _type))
            return

        if var is Metadata:
            if not hasattr(self.groups, metadata.group):
                self.groups[group] = {}
            
            self.groups[group][name] = metadata
            return

        raise TypeError 

    def _get(self, group, name):
        if hasattr(self.groups, group):
            if hasattr(self.groups[group], name):
                return self.groups[group][name]
        
        raise KeyError

    def get(self, group, name, default = None):
        try:
            meta = self._get(group, name) 
        except KeyError:
            if default == None:
                raise KeyError
            else:
                return default

        if meta is set:
            raise TypeError

        return meta

    def remove(self, group, name, silent = False):
        try:
            meta = self._get(group, name)
            del meta
        except KeyError:
            if not silent:
                raise KeyError

    def _get_tag_metadata(self, group, name):
        meta = self._get(group, name)
        if meta is not set:
            raise TypeError
        return meta

    def set_tag(self, group, name):
        self.set(group, name, set(), TAG)

    def add_tag(self, group, name, tag):
        meta = self._get_tag_metadata(group, name)

        meta.append(tag)

    def has_tag(self, group, name, tag):
        return tag in self._get_tag_metadata(group, name)

    def remove_tag(self, group, name, tag, silent = False):
        if silent:
            self._get_tag_metadata(group, name).discard(tag)
        else:
            self._get_tag_metadata(group, name).remove(tag)

    def tags(self, group, name):
        return self._get_tag_metadata(group, name)

    def metadata(self):
        for group in groups.values():
            for meta in group.values():
                yield meta
