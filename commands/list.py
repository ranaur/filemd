import argparse
import builtins

import filemd
from util import *

import yaml
import json

def listJSONGroup(m, prefix):
    out = {}
    for group, name, value in m.metadatas():
        if group not in out:
            out[group] = {}
        out[group][name] = value
    print(json.dumps(out)) 

def listJSON(m, prefix):
    out = {}
    for group, name, value in m.metadatas():
        out[group + "." + name] = value
    print(json.dumps(out)) 

def listYAMLGroup(m, prefix):
    out = {}
    for group, name, value in m.metadatas():
        if group not in out:
            out[group] = {}
        out[group][name] = value
    print(yaml.dump(out, default_flow_style=False)) 

def listYAML(m, prefix):
    out = {}
    for group, name, value in m.metadatas():
        out[group + "." + name] = value
    print(yaml.dump(out, default_flow_style=False)) 

def listText(m, prefix):
    for group, name, value in m.metadatas():
        if type(value) is list:
            tags = "[" + ",".join(value) + "]"
            print(prefix + group + "." + name + "=" + tags)
        else:
            print(prefix + group + "." + name + "=" + str(value))

def listMetatag(m, prefix):
    for group, name, value in m.metadatas():
        if type(value) is list:
            for tag in value:
                print(prefix + group + "." + name + ":" + tag)
        else:
            print(prefix + group + "." + name + "=" + str(value))

formats = {
        "text" : listText,
        "metatag" : listMetatag,
        "yaml" : listYAML,
        "yamlg" : listYAMLGroup,
        "json" : listJSON,
        "jsong" : listJSONGroup,
}

def method(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    for filename in args.files:
        prefix = filename + ": " if len(args.files) > 1 else ""
        m.load(filename)
        formats[args.format](m, prefix)
    return 0

parser_get = builtins.subparsers.add_parser(__name__.rsplit(".")[-1], help='lists all the metadata')
parser_get.add_argument('--format', choices=list(formats.keys()) , default='text', help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=method)

