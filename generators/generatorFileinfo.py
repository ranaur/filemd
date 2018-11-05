import builtins
import os
import datetime

def method(m, args):
    filename = m.filename
    s = os.stat(filename)
    m.setMeta("file.size", s.st_size)
    m.setMeta("file.access_time", datetime.datetime.fromtimestamp(s.st_atime))
    m.setMeta("file.modification_time", datetime.datetime.fromtimestamp(s.st_mtime))
    m.setMeta("file.creation_time", datetime.datetime.fromtimestamp(s.st_ctime))
    m.setMeta("file.absolute_name", os.path.abspath(filename))
    m.setMeta("file.base_name", os.path.basename(filename))
    m.setMeta("file.prefix", os.path.splitext(filename)[0])
    m.setMeta("file.extension", os.path.splitext(filename)[1])


parser_generate_fileinfo = builtins.subparser_generate.add_parser('fileinfo', help='generate file info')
parser_generate_fileinfo.set_defaults(funcGenerate=method)

