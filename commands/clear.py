import argparse
import builtins

import filemd
from util import *

def method(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    for filename in args.files:
        m.load(filename)
        m.clear()
    return 0

parser_get = builtins.subparsers.add_parser(__name__.rsplit(".")[-1], help='removes all the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=method)

