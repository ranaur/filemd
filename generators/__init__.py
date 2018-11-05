import os
import importlib
import builtins

here = os.path.dirname(__file__)
__all__ = []

builtins.generateFunctions = []

for fn in os.listdir(here):
    if fn.startswith("generator") and fn.endswith(".py") and fn != "generators.py":
        modname = fn[:-3]
        mod = importlib.import_module("." + modname, __package__)
        __all__.append(modname)
        builtins.generateFunctions.append(mod.method)

#for module in os.listdir(os.path.dirname(__file__)):
#    if module == '__init__.py' or module[-3:] != '.py' or not module.startswith("generator"):
#        continue
#    print module[:-3]
#    __import__(module[:-3], locals(), globals())
#del module

