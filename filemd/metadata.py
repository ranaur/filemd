#from pprint import pprint

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
        self.__timestamp = timestamp

    @property
    def timestamp(self):
        return self.__timestamp
    @timestamp.setter
    def timestamp(self, value = None):
        self.__timestamp = value if value is not None else datetime.datetime.now()
        
    def touch(self):
        self.timestamp


class Metadata(Timestamped):
    def __init__(self, var, name = None, value = None, type_ = DETECT, timestamp = None):
        if var is Metadata:
            super().__init__(var.timestamp)
            self.group = var.group
            self.name = var.name
            self.type = var.type
            self.value = var.value
            self.timestamp = var.timestamp
        else:
            super().__init__(timestamp)
            self.group = var
            self.name = name
            self.value = value
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

    def __str__(self):
        return "Metadata(group = '" + self.group + "', name='" + self.name + "', value = '" + str(self.value) + "', type = " + str(self.type) + ", timestamp = " + str(self.timestamp) + ")"

class Tag(Timestamped):
    def __init__(self, var, type_ = DETECT, timestamp = None):
        if type(var) is Tag:
            super().__init__(var.timestamp)
            self.value = var.value
            self.type = var.type
            self.timestamp = var.timestamp
        else:
            super().__init__(timestamp)
            self.value = var
            self.type = type_
            self.timestamp = timestamp

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

    def __str__(self):
        return "Tag(value = '" + str(self.value) + "', type = " + str(self.type) + ", timestamp = " + self.timestamp + ")"

class MetadataList():
    def __init__(self, tree = None):
        if tree is None:
            self.__groups = {}
        else:
            self.__groups = tree

    def merge(self, otherlist):
        for ol_group in otherlist.__groups:
            for ol_name in otherlist.__groups[ol_group]:
                ol_md = otherlist._get(ol_group, ol_name) 
                try:
                    my_md = self._get(ol_group, ol_name) 

                    if my_md.value == ol_md.value and my_md.type == my_md.type:
                        return
                    if ol_md.timestamp < my_md.timestamp:
                        return
                        
                except KeyError:
                    pass
                    
                self.set(Metadata(ol_md.group, ol_md.name, ol_md.value, ol_md.timestamp))
                    

    def set(self, var, name = None, value = None, _type = DETECT):
        if type(var) is list: # List of metadatas
            if len(var) == 0:
                return

            if type(var[0]) is Metadata:
                for v in var:
                    self.set(v)
                return

            if type(var[0]) is list:
                for v in var:
                    group = v[0]
                    name = v[1]
                    value = v[2]
                    _type = v[3] if len(v) == 4 else DETECT
                    self.set(Metadata(group, name, value, _type))
                return


        if type(var) is str and type(name) is str and value is not None:
            self.set(Metadata(var, name, value, _type))
            return

        if type(var) is Metadata:
            if var.group not in self.__groups:
                self.__groups[var.group] = {}
            group = self.__groups[var.group]
            group[var.name] = var
            return

        raise TypeError 

    def _get(self, group, name):
        if group in self.__groups:
            if name in self.__groups[group]:
                return (self.__groups[group])[name]
        raise KeyError

    def get(self, group, name, default = None):
        try:
            meta = self._get(group, name) 
        except KeyError:
            if default is None:
                raise KeyError
            else:
                return default

        if type(meta.value) is dict:
            raise TypeError

        return meta.value

    def get_timestamp(self, group, name):
        meta = self._get(group, name) 

        return meta.timestamp

    def remove(self, group, name, silent = False):
        try:
            self._get(group, name)
            del (self.__groups[group])[name]
        except KeyError:
            if not silent:
                raise KeyError

    def _get_tag_metadata(self, group, name):
        meta = self._get(group, name)
        if type(meta.value) is not dict:
            raise TypeError
        return meta

    def set_tag(self, group, name):
        self.set(group, name, {}, TAG)

    def get_tag_timestamp(self, group, name, tag):
        meta = self._get_tag_metadata(group, name).value
        tag_ = meta[tag]
        return tag_.timestamp

    def add_tag(self, group, name, tag):
        
        meta = self._get_tag_metadata(group, name)
        
        tags = meta.value
        if type(tag) is Tag:
            tags[tag] = tag
        elif type(tag) is list or type(tag) is set:
            for newtag in tag:
                if type(newtag) is Tag:
                    tags[newtag.value] = newtag
                else:
                    tags[newtag] = Tag(newtag)
        else:
            tags[tag] = Tag(tag)
        meta.touch()
        
    def has_tag(self, group, name, tag):
        return tag in self._get_tag_metadata(group, name).value

    def remove_tag(self, group, name, tag, silent = False):
        try:
            meta = self._get_tag_metadata(group, name)
            del meta.value[tag]
            meta.touch()
        except KeyError:
            if not silent:
                raise KeyError

    def tags(self, group, name):
        for tag in self._get_tag_metadata(group, name).value.keys():
            yield tag

    def tags_raw(self, group, name):
        for tag in self._get_tag_metadata(group, name).value.itens():
            yield tag

    def metadatas(self):
        for group in self.__groups.values():
            for meta in group.values():
                if type(meta.value) is dict:
                    yield (meta.group, meta.name, meta.value.keys())
                else:
                    yield (meta.group, meta.name, meta.value)

    def metadatas_raw(self):
        for group in self.__groups.values():
            for meta in group.values():
                yield meta

    def count(self):
        res = 0
        for group in self.__groups.values():
            res = res + len(group)
        return res
     
    def __str__(self):
        res = 'MetadataList:\n'
        for group, name, value in self.metadatas():
            res = res + '\t' + group + '.' + name + '=' + str(value) + '\n'
        return res
