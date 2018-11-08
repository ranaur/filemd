#!/bin/bash

./md.py set xxx.yyy "Hello World!" tests/gzip.py.gz
./md.py set yyy.xxx hello tests/gzip.py.gz
./md.py get yyy.xxx tests/gzip.py.gz
./md.py settag yyy.tag hello tests/gzip.py.gz
./md.py settag yyy.tag hello2 tests/gzip.py.gz
./md.py settag yyy.tag2 hello_more tests/gzip.py.gz
./md.py list --format=json tests/gzip.py.gz
./md.py list --format=jsong tests/gzip.py.gz
./md.py list --format=metatag tests/gzip.py.gz
./md.py list --format=metatag tests/gzip.py.gz tests/gzip.py.gz
./md.py list --format=yaml tests/gzip.py.gz
./md.py list --format=yamlg tests/gzip.py.gz
./md.py list tests/gzip.py.gz
./md.py list tests/gzip.py.gz tests/gzip.py.gz
./md.py listtag yyy.tag --format=json tests/gzip.py.gz
./md.py listtag yyy.tag --format=tags tests/gzip.py.gz
./md.py listtag yyy.tag --format=text tests/gzip.py.gz
./md.py listtag yyy.tag --format=yaml tests/gzip.py.gz
./md.py removetag yyy.tag hello2 tests/gzip.py.gz
./md.py remove yyy.tag tests/gzip.py.gz
./md.py clear tests/gzip.py.gz
