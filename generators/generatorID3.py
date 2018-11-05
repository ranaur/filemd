import mutagen
from pprint import pprint
def method(m, args):
    filename = m.filename
    #mime = m.getMeta("filetype.mime", "noMIME")
    #if mime == "noMIME":
    #    return
    #
    #if mime.startswith("audio/"):
    id3 = mutagen.File(filename, easy=True)
    if not id3 is None:
        for key in list(id3.keys()):
            value = id3[key]
            if type(value) is list:
                value = "".join(value)
            if type(value) is str:
                value = value.encode('utf8')
            try:
                value = int(value)
            except ValueError:
                pass

            m.setMeta("id3."+str(key), value)

name = 'id3'
description='generate id3 info'


