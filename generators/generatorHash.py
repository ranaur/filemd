from util.identity import hashFile
import hashlib

def method(m, args):
    filename = m.filename
    m.setMeta("hash.md5", hashFile(filename, hashlib.md5()))
    m.setMeta("hash.sha1", hashFile(filename, hashlib.sha1()))
    m.setMeta("hash.sha224", hashFile(filename, hashlib.sha224()))
    m.setMeta("hash.sha256", hashFile(filename, hashlib.sha256()))
    m.setMeta("hash.sha384", hashFile(filename, hashlib.sha384()))
    m.setMeta("hash.sha512", hashFile(filename, hashlib.sha512()))

name = 'hash'
description='generate hash'

