import os
import importlib

here = os.path.dirname(__file__)
__all__ = ["modules"]

modules = []

for fn in os.listdir(here):
    if fn.endswith(".py") and fn not in ["__init__.py"]:
        modname = fn[:-3]
        mod = importlib.import_module("." + modname, __package__)
        __all__.append(modname)
