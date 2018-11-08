import argparse
import builtins
import filemd

from util import *

def metadataSet(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    for filename in args.files:
        m.load(filename)
        group, name = name2groupname(args.name)
        m.set(group, name, args.value)
        m.save()
    return 0

parser_set = builtins.subparsers.add_parser('set', help='sets a name/value metadata')
parser_set.add_argument('name', type=str, help='name of the metadata')
parser_set.add_argument('value', type=str, help='value of the metadata')
parser_set.add_argument('files', nargs='+', help='files to process')
parser_set.set_defaults(func=metadataSet)
