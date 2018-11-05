import filetype
def method(m, args):
    filename = m.filename
    kind = filetype.guess(filename)
    if kind is None:
        print('Cannot guess file type!')
        return

    m.setMeta("filetype.extension",  kind.extension)
    m.setMeta("filetype.mime",  kind.mime)

parser_generate_filetype = subparser_generate.add_parser('filetype', help='generate type/mime info')
parser_generate_filetype.set_defaults(funcGenerate=method)

