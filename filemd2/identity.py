import os
import datetime
import filetype
import hashlib

class Identity:
    def __init__(self, *args):
        self.__file_validated = False
        self.__file= args["file"] if hasattr(args, "file") else None

        self.__filename = args["filename"] if hasattr(args, "filename") else self.get_filename()
        self.__md5 = args["md5"] if hasattr(args, "md5") else self.get_md5()
        self.__size = args["size"] if hasattr(args, "size") else self.get_size()
        self.__mime = args["mime"] if hasattr(args, "mime") else self.get_mime()
        self.__extension = args["extension"] if hasattr(args, "extension") else self.get_extension()
        self.__fullpath = args["fullpath"] if hasattr(args, "fullpath") else self.get_fullpath()
        self.__atime = args["atime"] if hasattr(args, "atime") else self.get_atime()
        self.__ctime = args["ctime"] if hasattr(args, "ctime") else self.get_ctime()
        self.__mtime = args["mtime"] if hasattr(args, "mtime") else self.get_mtime()

    def _validate_file(self):
        if self.__file_validated: 
            return

        if self.__file == None:
            raise ArgumentError

        if not os.path.isfile(self.__file):
            raise FileNotFoundError

        self.__file_validated = True

    def get_filename(self):
        self.__md5 = args["md5"] if hasattr(args, "md5") else self._load_md5()
        self.__size = args["size"] if hasattr(args, "size") else self._load_size()
        self.__mime = args["mime"] if hasattr(args, "mime") else self._load_mime()
        self.__fullpath = args["fullpath"] if hasattr(args, "fullpath") else self._load_fullpath()
        self.__atime = args["atime"] if hasattr(args, "atime") else self._load_atime()
        self.__ctime = args["ctime"] if hasattr(args, "ctime") else self._load_ctime()
        self.__mtime = args["mtime"] if hasattr(args, "mtime") else self._load_mtime()


    def _load_md5(self):
        if hasattr(self, "__md5"):
            return
        self.__md5 = self._hash()

    def _load_size(self):
       self.__size = datetime.datetime.fromtimestamp(self._stat().st_size)

    def __guess(self):
        if hasattr(self, "__guess"):
            return
        self.__guess = filetype.guess(self.__file)

    def _load_mime(self):
        if hasattr(self, "__mime"):
            return

        self.__guess()
        if guess is None:
            self.__mime = "application/octet-stream"
        else:
            self.__mime =  kind.mime
        
    def _load_extension(self):
        if hasattr(self, "__extension"):
            return

        self.__guess()
        if guess is None:
            self.__extension = "Unknown extension ." + os.split(self.__file)[1]
        else:
            self.__extension =  kind.extension

    def _load_fullpath(self):
        self.__fullpath = os.path.abspath(self.__file)

    def _load_atime(self):
        self.__atime = datetime.datetime.fromtimestamp(self.__stat().st_atime)

    def _load_ctime(self):
        self.__ctime = datetime.datetime.fromtimestamp(self.__stat().st_ctime)

    def _load_mtime(self):
        self.__mtime = datetime.datetime.fromtimestamp(self.__stat().st_mtime)

    def __hash(algorithm):
        self._validate_file(self)
        with open(self.__file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                algorithm.update(chunk)
        return algorithm.hexdigest()

    def __stat(self):
        if not hasattr(self, "__stat"):
            self._validate_file(self)
            self.__stat = os.stat(self.__file)
        return self.__stat;

