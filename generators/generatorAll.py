import builtins
import sys

def method(m, args):
    pass # dummy to avoid recursion

def methodAll(m, args):
    for method_to_call in builtins.generateFunctions:
        method_to_call(m, args)

name = 'all'
description='generate all info'

