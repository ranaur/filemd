# -*- coding: utf-8 -*-

import pytest
import time
from pprint import pprint
import os

from filemd2 import *

TEST_FILE = "testfile"
class TestMetadata(object):
    def test_driver(self):
        fm = FileMetadata()
        fm.add_driver(DriverRemoraYAML.DriverRemoraYAML())
        d = fm.list_drivers()
        assert len(d) == 1
        assert d["DriverRemoraYAML"][1] == "RW"
        assert type(d["DriverRemoraYAML"][0]) is drivers.DriverRemoraYAML.DriverRemoraYAML

        fm.del_driver(DriverRemoraYAML.DriverRemoraYAML())
        d = fm.list_drivers()
        assert len(d) == 0

        fm.add_driver(DriverRemoraYAML.DriverRemoraYAML(), read_only = True)
        d = fm.list_drivers()
        assert len(d) == 1
        assert d["DriverRemoraYAML"][1] == "R"

        fm.del_driver(DriverRemoraYAML.DriverRemoraYAML())
        d = fm.list_drivers()
        assert len(d) == 0

        fm.add_driver(DriverRemoraYAML.DriverRemoraYAML(), write_only = True)
        d = fm.list_drivers()
        assert len(d) == 1
        assert d["DriverRemoraYAML"][1] == "W"

        fm.del_driver("DriverRemoraYAML")
        d = fm.list_drivers()
        assert len(d) == 0

    def create_test_file(self, test_file = TEST_FILE):
        with open(test_file, "w+") as fp:
            fp.write("Test File")
        
    def clear_test_file(self, test_file = TEST_FILE):
        try:
            os.remove(test_file)
        except:
            pass
        
    def test_load(self):
        self.clear_test_file()
        with pytest.raises(FileNotFoundError):
            fm = FileMetadata(TEST_FILE)
        
        self.create_test_file()
        fm = FileMetadata(TEST_FILE)
        fm.add_driver(DriverRemoraYAML.DriverRemoraYAML())
        fm.set("group", "name", "value")
        fm.save()
        
        fm = FileMetadata()
        fm.add_driver(DriverRemoraYAML.DriverRemoraYAML(), read_only = True)
        fm.load(TEST_FILE)
        #print(fm)
        assert fm.get("group", "name") == "value"

        fm.add_driver(DriverRemoraYAML.DriverRemoraYAML(), write_only = True)
        fm.clear()
        
        self.clear_test_file()

    
    def test_get_set_metadata(self):
        fm = FileMetadata()
        
        assert fm.get("group", "name", "default") == "default"
        with pytest.raises(KeyError):
            fm.get("group", "name")

        fm.set("group", "name", "value")
        assert fm.get("group", "name") == "value"

        fm.remove("group", "name")
        assert fm.get("group", "name", "default") == "default"
        with pytest.raises(KeyError):
            fm.get("group", "name")

    def test_get_set_tag(self):
        fm = FileMetadata()
        fm.set_tag("group", "tags")
        fm.add_tag("group", "tags", "first tag")
        fm.add_tag("group", "tags", "second tag")
        assert fm.has_tag("group", "tags", "first tag")
        assert fm.has_tag("group", "tags", "second tag")
        assert not fm.has_tag("group", "tags", "non-existent tag")
        fm.remove_tag("group", "tags", "second tag")
        assert not fm.has_tag("group", "tags", "second tag")
        assert fm.has_tag("group", "tags", "first tag")
        
        assert "first tag" in fm.tags("group", "tags")
        with pytest.raises(TypeError):
            fm.get("group", "tags")

        fm.remove("group", "tags")
        assert fm.get("group", "tags", "default") == "default"
        with pytest.raises(KeyError):
            fm.get("group", "tags")
         
    def test_timestamp(self):
        fm = FileMetadata()
        fm.set("time", "older name", "older value")
        time.sleep(1) 
        fm.set("time", "newer name", "newer value")
        assert fm.get_timestamp("time", "older name") < fm.get_timestamp("time", "newer name")
        fm.set_tag("time", "timetag")
        fm.add_tag("time", "timetag", "old tag")
        time.sleep(1) 
        fm.add_tag("time", "timetag", "new tag")
        assert fm.get_tag_timestamp("time", "timetag", "old tag") < fm.get_tag_timestamp("time", "timetag", "new tag")
        
    def test_metadata(self):
        fm = FileMetadata()
        fm.set("metadata", "first", "first value")
        fm.set("metadata", "first", "first value (again)")
        fm.set("metadata", "second", "second value")
        i = 0
        for md in fm.metadatas():
            i = i + 1
        assert i == 2

    def test_metadata_raw(self):
        fm = FileMetadata()
        fm.set("metadata", "first", "first value")
        fm.set("metadata", "first", "first value (again)")
        fm.set("other.metadata", "first", "other first value")
        fm.set("metadata", "second", "second value")
        i = 0
        for md in fm.metadatas_raw():
            i = i + 1
        assert i == 3
        
    def test_merge(self):
        fm1 = FileMetadata()
        fm1.set("merge", "first", "first value")
        fm1.set("merge", "second", "second value")
        time.sleep(1) 
        fm2 = FileMetadata()
        fm2.set("merge", "first", "first value (merged)")
        fm2.set("merge", "third", "third value")

        fm1.merge(fm2)
        i = 0
        assert fm1.count() == 3

    def test_count(self):
        fm = FileMetadata()
        fm.set("count", "first", "first value")
        fm.set("count", "second", "second value")
        fm.set("count2", "first", "first value")
        fm.set("count2", "second", "second value")
        assert fm.count() == 4

    def test_set_array(self):
        arr = [
            ['group one', 'name one', 'value one'],
            ['group two', 'name two', 'value two'],
            ['group three', 'name three', 'value three'],
        ]
        fm = FileMetadata()
        fm.set(arr)
        assert fm.get('group one', 'name one') == 'value one'
        assert fm.get('group two', 'name two') == 'value two'
        assert fm.get('group three', 'name three') == 'value three'

    def test_set_array_meta(self):
        arr = [
            Metadata('group one', 'name one', 'value one'),
            Metadata('group two', 'name two', 'value two'),
            Metadata('group three', 'name three', 'value three'),
        ]
        fm = FileMetadata()
        fm.set(arr)
        assert fm.get('group one', 'name one') == 'value one'
        assert fm.get('group two', 'name two') == 'value two'
        assert fm.get('group three', 'name three') == 'value three'
        
# set array os metadatas and array 4xN 3xN
# count
    def __def__(self):
        self.clean_test_file()
