import argparse
import builtins

import filemd
from util import *

def method(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    for filename in args.files:
        m.load(filename)
        group, name = name2groupname(args.name)
        m.remove(group, name)
        m.save()
    return 0

parser_get = builtins.subparsers.add_parser(__name__.rsplit(".")[-1], help='removes a metadata')
parser_get.add_argument('name', type=str, help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=method)

