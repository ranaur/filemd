import argparse
import builtins

import filemd
from util import *

def method(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    for filename in args.files:
        m.load(filename)
        group, name = name2groupname(args.name)
        try:
            value = m.get(group, name)
            if len(args.files) == 1:
                print((str(value)))
            else:
                print((filename + ": " + str(value)))
        except KeyError:
            print("key {} not found".format(args.name))
            return 1
    return 0

parser_get = builtins.subparsers.add_parser(__name__.rsplit(".")[-1], help='gets a metadata')
parser_get.add_argument('name', type=str, help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=method)

