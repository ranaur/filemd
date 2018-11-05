import builtins
import piexif

def method(m, args):
    exifDictionary = {
        256: "ImageWidth",
        257: "ImageLength",
        258: "BitsPerSample",
        #259: "Compression",
        #262: "PhotometricInterpretation",
        274: ("Orientation", {1:"Top-left", 2:"Top-right", 3:"Bottom-Right", 4:"Bottom-Left", 5:"Left-Top", 6:"Right-Top", 7:"Right-Bottom", 8:"Left-Bottom"} ),
        277: "SamplesPerPixel",
        #284: "PlanarConfiguration",
        #530: "YCbCrSubSampling",
        #531: "YCbCrPositioning",
        282: "XResolution",
        283: "YResolution",
        296: ("ResolutionUnit", {2:"inches", 3:"centimeters"}),
        306: "DateTime",
        270: "ImageDescription",
        271: "Make",
        272: "Model",
        305: "Software",
        315: "Artist",
        33432: "Copyright",
    }
    filename = m.filename
    mime = m.getMeta("filetype.mime", "noMIME")
    if mime == "noMIME":
        return

    if mime in ["image/jpeg"]:
        exif_dict = piexif.load(filename)
        ifd = exif_dict['0th']
        for tag in ifd:
            if tag in list(exifDictionary.keys()):
                value = exifDictionary[tag]
                if type(value) is set or type(value) is list or type(value) is tuple:
                    tagname = value[0]
                    tagvalue = value[1][ifd[tag]]
                else:
                    tagname = value
                    tagvalue = ifd[tag]

                if type(tagvalue) is tuple:
                    tagvalue = tagvalue[0]/tagvalue[1]

                m.setMeta("exif0th."+str(tagname), tagvalue)

name = 'exif'
description='generate exif info'
