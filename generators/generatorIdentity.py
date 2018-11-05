import os
import datetime
import filetype
import hashlib

def hashFile(fname, algorithm):
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            algorithm.update(chunk)
    return algorithm.hexdigest()

def identity(filename):
    res = {}
    s = os.stat(filename)
    res["identity.size"] = s.st_size
    res["identity.access_time"] = datetime.datetime.fromtimestamp(s.st_atime)
    res["identity.modification_time"] = datetime.datetime.fromtimestamp(s.st_mtime)
    res["identity.creation_time"] = datetime.datetime.fromtimestamp(s.st_ctime)
    res["identity.absolute_name"] = os.path.abspath(filename)
    res["identity.base_name"] = os.path.basename(filename)
    res["identity.prefix"] = os.path.splitext(filename)[0]
    res["identity.extension"] = os.path.splitext(filename)[1]

    kind = filetype.guess(filename)
    if kind is None:
        res["identity.extension"] = "Unknown"
        res["identity.mime"] = "application/octet-stream"
    else:
        res["identity.extension"] =  kind.extension
        res["identity.mime"] =  kind.mime
    res["identity.md5"] = hashFile(filename, hashlib.md5())
    res["identity.sha512"] = hashFile(filename, hashlib.sha512())
    return res

def method(m, args):
    info = identity(m.filename)
    for key, value in info.items():
        m.setMeta(key, value)
    #for key in info:
        #print("{} : {} = {}".format(key, type(key), info[key]))
    #    m.setMeta(key, info[key])

name = 'identity'
description='generate basic info'

