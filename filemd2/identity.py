import inspect

import os
import datetime
import filetype
import hashlib

class Identity:
    def __init__(self, **args):
        self.__file_validated = False
        self.file= args["file"] if "file" in args else None
        self.md5 = args["md5"] if "md5" in args else self._load_md5()
        self.size = args["size"] if "size" in args else self._load_size()
        self.mime = args["mime"] if "mime" in args else self._load_mime()
        self.fullpath = args["fullpath"] if "fullpath" in args else self._load_fullpath()
        self.atime = args["atime"] if "atime" in args else self._load_atime()
        self.ctime = args["ctime"] if "ctime" in args else self._load_ctime()
        self.mtime = args["mtime"] if "mtime" in args else self._load_mtime()

    def _validate_file(self):
        if self.__file_validated: 
            return

        if self.file == None:
            raise ArgumentError

        if not os.path.isfile(self.file):
            raise FileNotFoundError

        self.file_validated = True

    def _load_md5(self):
        if hasattr(self, "md5"):
            return
        return self.__hash()

    def _load_size(self):
        return self.__stat().st_size

    def __guess(self):
        if hasattr(self, "__guess_"):
            return
        self.__guess_ = filetype.guess(self.file)

    def _load_mime(self):
        if hasattr(self, "mime"):
            return

        self.__guess()
        return self.__guess_.mime if hasattr(self.__guess_, "mime") else "application/octet-stream"
        
    def _load_extension(self):
        if hasattr(self, "__extension"):
            return

        self.__guess()
        return self.__guess_.extension if hasattr(self.__guess_, "mime") else "Unknown extension ." + os.split(self.file)[1]

    def _load_fullpath(self):
        return os.path.abspath(self.file)

    def _load_atime(self):
        return datetime.datetime.fromtimestamp(self.__stat().st_atime)

    def _load_ctime(self):
        return datetime.datetime.fromtimestamp(self.__stat().st_ctime)

    def _load_mtime(self):
        return datetime.datetime.fromtimestamp(self.__stat().st_mtime)

    def __hash(self):
        h = hashlib.new("md5")
        self._validate_file()
        with open(self.file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def __stat(self):
        if not hasattr(self, "__stat_"):
            self._validate_file()
            self.__stat_ = os.stat(self.file)
        return self.__stat_;


    def __str__(self):
        return "Identity<file = %s md5 = %s>" % (self.file, self.md5)

