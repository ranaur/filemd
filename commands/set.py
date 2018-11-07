import argparse
import builtins
import filemd2

def metadataSet(args):
    m = filemd2.FileMetadata()
    m.add_driver(DriverRemoraYAML())
    for filename in args.files:
        group, name = name2groupname(args.name)
        m.set(group, name, args.value)
    m.save()

parser_set = builtins.subparsers.add_parser('set', help='sets a name/value metadata')
parser_set.add_argument('name', type=str, help='name of the metadata')
parser_set.add_argument('value', type=str, help='value of the metadata')
parser_set.add_argument('files', nargs='+', help='files to process')
parser_set.set_defaults(func=metadataSet)
