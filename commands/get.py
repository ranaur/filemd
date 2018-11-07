import argparse
import builtins

import filemd2

def metadataGet(args):
    m = filemd2.FileMetadata()
    m.add_driver(filemd2.DriverRemoraYAML.DriverRemoraYAML())
    for filename in args.files:
        group, name = name2groupname(args.name)
        try:
            value = m.get(group, name)
            if len(args.files) == 1:
                print((str(value)))
            else:
                print((filename + ": " + str(value)))
        except KeyError:
            print("key {} not found".format(name))


parser_get = builtins.subparsers.add_parser('get', help='gets a metadata')
parser_get.add_argument('name', type=str, help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=metadataGet)

