import builtins
import taglib
from pprint import pprint
def method(m, args):
    filename = m.filename
    import taglib
    id3 = taglib.File(filename)
    if not id3 is None:
        for key, value in id3.tags:
            if type(value) is list:
                value = "".join(value)
            if type(value) is str:
                value = value.encode('utf8')
            try:
                value = int(value)
            except ValueError:
                pass

            m.setMeta("taglib."+str(key), value)

parser_generate_taglib = subparser_generate.add_parser('taglib', help='generate id3 info with taglib')
parser_generate_taglib.set_defaults(funcGenerate=method)


