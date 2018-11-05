import filetype
def method(m, args):
    filename = m.filename
    kind = filetype.guess(filename)
    if kind is None:
        print('Cannot guess file type!')
        return

    m.setMeta("filetype.extension",  kind.extension)
    m.setMeta("filetype.mime",  kind.mime)

name = 'filetype'
description = 'generate type/mime info'

