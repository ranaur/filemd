import builtins
from PIL import Image
import imagehash
def method(m, args):
    filename = m.filename
    mime = m.getMeta("filetype.mime", "noMIME")
    if mime == "noMIME":
        return

    if mime.startswith("image/"):
        image = Image.open(filename)
        m.setMeta("imagehash.average", str(imagehash.average_hash(image)))
        m.setMeta("imagehash.phash", str(imagehash.phash(image)))
        m.setMeta("imagehash.dhash", str(imagehash.dhash(image)))
        m.setMeta("imagehash.whash-haar", str(imagehash.whash(image)))
        m.setMeta("imagehash.whash-db4", str(imagehash.whash(image, mode='db4')))

name = 'imagehash'
description='generate imagehash info'


