import builtins
from pytineye import TinEyeAPIRequest
from pprint import pprint

api = TinEyeAPIRequest('http://api.tineye.com/rest/', 'your_public_key', 'your_private_key')

def method(m, args):
    filename = m.filename
    if args.tineye:
        with open(filename, 'rb') as fp:
            print("File: " + filename)
            data = fp.read()
            resp = api.search_data(data=data)
            for match in resp:
                pprint(match)
                for backlink in match.backlinks:
                    pprint(backlink)

parser_generate_tineye = builtins.subparser_generate.add_parser('tineye', help='generate tineye info')
parser_generate_tineye.add_argument('--tineye', action='store_true')
parser_generate_tineye.set_defaults(funcGenerate=method)

