import os
import importlib
import builtins

here = os.path.dirname(__file__)
__all__ = ["modeules"]

modules = []

for fn in os.listdir(here):
    if fn.startswith("generator") and fn.endswith(".py") and fn != "generators.py":
        modname = fn[:-3]
        mod = importlib.import_module("." + modname, __package__)
        __all__.append(modname)
        modules.append(mod)

