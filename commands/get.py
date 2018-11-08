import argparse
import builtins

import filemd2
from util import *

def metadataGet(args):
    m = filemd2.FileMetadata(filemd2.get_driver(args.driver))
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

parser_get = builtins.subparsers.add_parser('get', help='gets a metadata')
parser_get.add_argument('name', type=str, help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=metadataGet)

