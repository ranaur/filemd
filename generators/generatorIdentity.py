from util.identity import identity

def method(m, args):
    info = identity(m.filename)
    for key, value in info.items():
        m.setMeta(key, value)

name = 'identity'
description='generate basic info'

