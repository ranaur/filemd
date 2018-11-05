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

name = 'hash'
description='generate hash'

