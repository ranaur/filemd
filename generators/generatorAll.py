import builtins
import sys

def method(m, args):
    pass # dummy to avoid recursion

def methodAll(m, args):
#    moduleinfo = dir(sys.modules[__name__])
#    for method in moduleinfo:
#        if method.startswith("metadataGenerate") and method != 'metadataGenerate' and method != "metadataGenerateAll":
    for method_to_call in builtins.generateFunctions:
        method_to_call(m, args)

parser_generate_all = subparser_generate.add_parser('all', help='generate all info')
parser_generate_all.set_defaults(funcGenerate=methodAll)

