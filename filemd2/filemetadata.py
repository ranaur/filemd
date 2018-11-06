class FileMetadata:
    def __init__(self, var = None):
        self.__metadatas = MetadataList()
        self.__itentity = None
        self.__read_drivers = []
        self.__write_drivers = []

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
                if d.name == driver:
                    self.__read_drivers.remove(d)
            return

        if isinstance(driver, Driver):
            for d in self.__read_drivers:
                if d.name == driver.name:
                    self.__read_drivers.remove(d)
            return

    def del_write_driver(self, driver):
        if type(driver) == str:
            for d in self.__write_drivers:
                if d.name == driver:
                    self.__write_drivers.remove(d)
            return

        if isinstance(driver, Driver):
            for d in self.__write_drivers:
                if d.name == driver.name:
                    self.__write_drivers.remove(d)
            return

    def list_drivers(self):
        res = {}
        for d in self.__read_drivers:
            res[d.name] = [d, "R"]
        for d in self.__write_drivers:
            if hasattr(res, d.name):
                res[d.name] = [d, "RW"]
            else:
                res[d.name] = [d, "W"]

    def load_metadata(self, var):
        if var is str: 
            var = Identity(file = var)

        if var is not Identity:
            raise TypeError

        self.__identity = var

        for d in self.__read_drivers:
            self.__metadatas.merge(d.load_metadata(var))

    def set(self):
        raise NotImplemented

    def get(self):
        raise NotImplemented

    def remove(self):
        raise NotImplemented

    def set_tag(self):
        raise NotImplemented

    def add_tag(self):
        raise NotImplemented

    def has_tag(self):
        raise NotImplemented

    def remove_tag(self):
        raise NotImplemented

    def tags(self):
        raise NotImplemented

    def metadata(self):
        raise NotImplemented
