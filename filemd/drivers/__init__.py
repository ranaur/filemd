import os
import importlib

here = os.path.dirname(__file__)
__all__ = ["modules"]

from .driver import Driver

modules = []
drivers_classes = {}

for fn in os.listdir(here):
    if fn.endswith(".py") and fn not in ["__init__.py", "driver.py"]:
        modname = fn[:-3]
        mod = importlib.import_module("." + modname, __package__)
        drivers_classes[modname] = mod.driver_class
        __all__.append(modname)
        modules.append(mod)

def get_driver(name):
    if type(name) in [list, set, tuple]:
        res = ()
        for n in name:
            res.add(drivers_classes[name]())
        return res

    return drivers_classes[name]()
