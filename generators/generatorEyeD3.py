import builtins
import eyed3
def method(m, args):
    filename = m.filename
    mime = m.getMeta("filetype.mime", "noMIME")
    if mime == "noMIME":
        return

    if mime.startswith("audio/"):
        id3 = eyed3.load(filename)
        m.setMeta("eyeD3.title", id3.tag.title)
        m.setMeta("eyeD3.artist", id3.tag.artist)
        m.setMeta("eyeD3.album", id3.tag.album)
        m.setMeta("eyeD3.album_artist", id3.tag.album_artist)
        m.setMeta("eyeD3.track_num", id3.tag.track_num[0])

parser_generate_id3 = subparser_generate.add_parser('eyeD3', help='generate id3 info using eyeD3')
parser_generate_id3.set_defaults(funcGenerate=method)


