import builtins
import magic
def method(m, args):
    filename = m.filename
    m.setMeta("filetype.magic", magic.from_file(filename))
    f = magic.Magic(mime=True, uncompress=False)
    m.setMeta("filetype.magicMime", f.from_file(filename))
    f = magic.Magic(mime=False, uncompress=True)
    m.setMeta("filetype.magicUncompress", f.from_file(filename))
    f = magic.Magic(mime=True, uncompress=True)
    m.setMeta("filetype.magicUncompressMime", f.from_file(filename))

name = 'magic'
description = 'generate type/mime info based on magic file'

