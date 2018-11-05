import builtins
from filemd import Metadata, metadata, savers
import argparse
import sys
from pprint import pprint

def metadataGenerateAll(m, args):
    moduleinfo = dir(generators)
    for method in moduleinfo:
        if method.startswith("metadataGenerate") and method != 'metadataGenerate' and method != "metadataGenerateAll":
            method_to_call = getattr(sys.modules[__name__], method)
            method_to_call(m, args)

def metadataGenerate(args):
    for filename in args.files:
        m = metadata(filename)
        args.funcGenerate(m, args)
        m.save()

def metadataSet(args):
    for filename in args.files:
        m = metadata(filename)
        m.setMeta(args.name, args.value)
        m.save()

def metadataGet(args):
    for filename in args.files:
        m = metadata(filename)
        value = m.getMeta(args.name)
        if len(args.files) == 1:
            print((str(value)))
        else:
            print((filename + ": " + str(value)))

def metadataRemove(args):
    for filename in args.files:
        m = metadata(filename)
        m.remove(args.name)
        m.save()

def metadataSettag(args):
    for filename in args.files:
        m = metadata(filename)
        for tag in args.tags.split(","):
            m.setTag(args.taggroup, tag)
        m.save()

def metadataUnsettag(args):
    for filename in args.files:
        m = metadata(filename)
        for tag in args.tags.split(","):
            m.unsetTag(args.taggroup, tag)
        m.save()

def metadataClear(args):
    for filename in args.files:
        m = metadata(filename)
        m.clear()
        m.save()

def metadataList(args):
    for filename in args.files:
        m = metadata(filename)
        print((filename + ": "))
        pprint(m.list())

def metadataSavers(args):
    s = savers()
    pprint(s)


parser = argparse.ArgumentParser(description='command line metadata editor')
subparsers = parser.add_subparsers(
                )
# - add parameters
parser_set = subparsers.add_parser('set', help='sets a name/value metadata')
parser_set.add_argument('name', type=str, help='name of the metadata')
parser_set.add_argument('value', type=str, help='value of the metadata')
parser_set.add_argument('files', nargs='+', help='files to process')
parser_set.set_defaults(func=metadataSet)

parser_get = subparsers.add_parser('get', help='gets a metadata')
parser_get.add_argument('name', type=str, help='name of the metadata')
parser_get.add_argument('files', nargs='+', help='files to process')
parser_get.set_defaults(func=metadataGet)

parser_remove = subparsers.add_parser('remove', help='removes a metadata/taggroup')
parser_remove.add_argument('name', type=str, help='name of the metadata/taggroup')
parser_remove.add_argument('files', nargs='+', help='files to process')
parser_remove.set_defaults(func=metadataRemove)

parser_unsettag = subparsers.add_parser('unsettag', help='unsets a tag')
parser_unsettag.add_argument('taggroup', type=str, help='name of the taggroup')
parser_unsettag.add_argument('tags', type=str, help='comma separated list tags to unset')
parser_unsettag.add_argument('files', nargs='+', help='files to process')
parser_unsettag.set_defaults(func=metadataUnsettag)

parser_settag = subparsers.add_parser('settag', help='set a tag')
parser_settag.add_argument('taggroup', type=str, help='name of the taggroup')
parser_settag.add_argument('tags', type=str, help='comma separated list tags to set')
parser_settag.add_argument('files', nargs='+', help='files to process')
parser_settag.set_defaults(func=metadataSettag)

parser_clear = subparsers.add_parser('clear', help='remove all metadata info')
parser_clear.add_argument('files', nargs='+', help='files to process')
parser_clear.set_defaults(func=metadataClear)

parser_list = subparsers.add_parser('list', help='list all metadata')
parser_list.add_argument('files', nargs='+', help='files to process')
parser_list.set_defaults(func=metadataList)

parser_savers = subparsers.add_parser('savers', help='list all configured savers')
parser_savers.set_defaults(func=metadataSavers)

parser_generate = subparsers.add_parser('generate', help='generate metadata info based on file/content')

subparser_generate = parser_generate.add_subparsers()
builtins.subparser_generate = subparser_generate
parser_generate.add_argument('files', nargs='+', help='files to process')
parser_generate.set_defaults(func=metadataGenerate)

import generators

#parser_generate_fileinfo = subparser_generate.add_parser('filetype', help='generate type/mime info')
#parser_generate_fileinfo.set_defaults(funcGenerate=metadataGenerateFiletype)
#
#parser_generate_magic = subparser_generate.add_parser('magic', help='generate type/mime info based on magic file')
#parser_generate_magic.set_defaults(funcGenerate=metadataGenerateFiletype)
#
#parser_generate_magic = subparser_generate.add_parser('all', help='generate all info')
#parser_generate_magic.set_defaults(funcGenerate=metadataGenerateAll)
#
#parser_generate_exif = subparser_generate.add_parser('exif', help='generate exif info')
#parser_generate_exif.set_defaults(funcGenerate=metadataGenerateEXIF)

args = parser.parse_args()

import inspect
if (hasattr(args, 'func') and inspect.isfunction(args.func)):
    args.func(args)
else:
    parser.print_help()


