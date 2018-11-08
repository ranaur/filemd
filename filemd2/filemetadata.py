from .metadata import MetadataList
from .identity import Identity
from .drivers import Driver

from .metadata import DETECT
from .metadata import TEXT
from .metadata import NUMBER
from .metadata import DATETIME
from .metadata import DATA
from .metadata import TAG


class FileMetadata:
    def __init__(self, *args):
        self.__metadatas = MetadataList()
        self.__read_drivers = []
        self.__write_drivers = []
        self._init(args)

    def _init(self, var):
        if type(var) in [list, set, tuple]:
            for v in var:
                self._init(v)
            return

        if isinstance(var, Driver):
            self.add_driver(var)
            return

        if isinstance(var, Identity) or type(var) is str:
            self.load(var)
            return

        raise TypeError

    def add_driver(self, driver, read_only = False, write_only = False):
        if not isinstance(driver, Driver):
            raise TypeError

        if not read_only: # that is, writes
            self.__write_drivers.append(driver)
        if not write_only: # that is, reads
            self.__read_drivers.append(driver)

    def del_driver(self, driver, del_read_driver = True, del_write_driver = True):
        if del_read_driver:
            self.del_read_driver(driver)
        if del_write_driver:
            self.del_write_driver(driver)

    def del_read_driver(self, driver):
        if type(driver) == str:
            for d in self.__read_drivers:
                if d.name() == driver:
                    self.__read_drivers.remove(d)
            return

        if hasattr(driver, "name"):
            for d in self.__read_drivers:
                if d.name() == driver.name():
                    self.__read_drivers.remove(d)
            return
        raise TypeError

    def del_write_driver(self, driver):
        if type(driver) == str:
            for d in self.__write_drivers:
                if d.name() == driver:
                    self.__write_drivers.remove(d)
            return

        if hasattr(driver, "name"):
            for d in self.__write_drivers:
                if d.name() == driver.name():
                    self.__write_drivers.remove(d)
            return
            
        raise TypeError

    def list_drivers(self):
        res = {}
        for d in self.__read_drivers:
            res[d.name()] = [d, "R"]
        for d in self.__write_drivers:
            if d.name() in res:
                res[d.name()] = [d, "RW"]
            else:
                res[d.name()] = [d, "W"]
        return res

    def load(self, var):
        if type(var) is str: 
            var = Identity(file = var)

        if type(var) is not Identity:
            raise TypeError

        self.__identity = var
        self.__metadatas = MetadataList()

        for driver in self.__read_drivers:
            n = driver.load(var)
            self.__metadatas.merge(n)

    def save(self):
        for driver in self.__write_drivers:
            driver.save(self.__identity, self.__metadatas)

    def clear(self):
        for driver in self.__write_drivers:
            driver.clear(self.__identity)

    def __getattr__(self, name):
        #if name.startswith("_"):
        #    raise AttributeError
        
        return getattr(self.__metadatas, name)

    def __str__(self):
        # list_drivers(self) ..;
        return self.__metadatas.__str__()
