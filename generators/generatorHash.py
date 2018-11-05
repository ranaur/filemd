import builtins
import hashlib
def hashFile(fname, algorithm):
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            algorithm.update(chunk)
    return algorithm.hexdigest()

def method(m, args):
    filename = m.filename
    try:
        if not args.nomd5:
            m.setMeta("hash.md5", hashFile(filename, hashlib.md5()))
        if args.sha1 or args.all:
            m.setMeta("hash.sha1", hashFile(filename, hashlib.sha1()))
        if args.sha224 or args.all:
            m.setMeta("hash.sha224", hashFile(filename, hashlib.sha224()))
        if args.sha256 or args.all:
            m.setMeta("hash.sha256", hashFile(filename, hashlib.sha256()))
        if args.sha384 or args.all:
            m.setMeta("hash.sha384", hashFile(filename, hashlib.sha384()))
        if args.sha512 or args.all:
            m.setMeta("hash.sha512", hashFile(filename, hashlib.sha512()))
    except:
        m.setMeta("hash.md5", hashFile(filename, hashlib.md5()))

parser_generate_hash = builtins.subparser_generate.add_parser('hash', help='generate hash')
parser_generate_hash.add_argument('--nomd5', action='store_true', help='md5 is the default argument')
parser_generate_hash.add_argument('--sha1', action='store_true')
parser_generate_hash.add_argument('--sha224', action='store_true')
parser_generate_hash.add_argument('--sha256', action='store_true')
parser_generate_hash.add_argument('--sha384', action='store_true')
parser_generate_hash.add_argument('--sha512', action='store_true')
parser_generate_hash.add_argument('--all', action='store_true')
parser_generate_hash.set_defaults(funcGenerate=method)

