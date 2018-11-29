import argparse
import builtins

import filemd
from util import *

import yaml
import json

def listJSON(m, group, name, prefix):
    out = m.tags(group, name)
    print(json.dumps(list(out))) 

def listYAML(m, group, name, prefix):
    out = m.tags(group, name)
    print(yaml.dump(list(out), default_flow_style=False)) 

def listText(m, group, name, prefix):
    for value in m.tags(group, name):
        print(prefix + group + "." + name + "=" + str(value))

def listTags(m, group, name, prefix):
    for value in m.tags(group, name):
        print(prefix + str(value))

formats = {
        "text" : listText,
        "tags" : listTags,
        "yaml" : listYAML,
        "json" : listJSON,
}

def method(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    group, name = name2groupname(args.name)
    for filename in args.files:
        prefix = filename + ": " if len(args.files) > 1 else ""
        m.load(filename)
        formats[args.format](m, group, name, prefix)
    return 0

parser_get = builtins.subparsers.add_parser(__name__.rsplit(".")[-1], help='list all tags from a metadata')
parser_get.add_argument('--format', choices=list(formats.keys()) , default='text', help='name of the metadata')
parser_get.add_argument('name', type=str, help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=method)


