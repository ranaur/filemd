VERSION = '0.0.0'

from .metadataerror import *
from .metadata import Metadata
from .savers import loaded_savers

def savers():
    global loaded_savers
    res = []
    for saver in loaded_savers:
        res.append(saver.description())
    return res

def metadata(filename):
    global loaded_savers

    return Metadata(filename, loaded_savers)

#__all__ = ['metadata', 'Metadata', 'savers']
