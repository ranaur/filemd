import argparse
import builtins
import filemd

from util import *

def method(args):
    m = filemd.FileMetadata(filemd.get_driver(args.driver))
    for filename in args.files:
        m.load(filename)
        group, name = name2groupname(args.name)
        tags = args.tag.split(",")
        for t in tags:
            t = t.strip()
        m.set_tag(group, name, tags)
        m.save()
    return 0

parser_set = builtins.subparsers.add_parser(__name__.rsplit(".")[-1], help='sets a tag')
parser_set.add_argument('name', type=str, help='name of the metadata')
parser_set.add_argument('tag', type=str, help='tag to add (comma seprated)')
parser_set.add_argument('files', nargs='+', help='files to process')
parser_set.set_defaults(func=method)
