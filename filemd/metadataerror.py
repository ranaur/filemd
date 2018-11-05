class MetadataError(Exception):
    def __init__(self):
        self.value = "Generic Metadata Error"
    def __str__(self):
        return repr(self.value)

# metadata operation in a tag group or tag operation in a metadata
class MetadataNoMetaError(MetadataError):
    def __init__(self):
        self.value = "Name is not a metadata"

class MetadataNoTagError(MetadataError):
    def __init__(self):
        self.value = "Name is not a tag"

class MetadataNoNameError(MetadataError):
    def __init__(self):
        self.value = "Name is not found"

class MetadataNoFileError(MetadataError):
    def __init__(self):
        self.value = "Filename is not found"

class MetadataInvalidFormatError(MetadataError):
    def __init__(self):
        self.value = "Invalid metadata format file"

class MetadataInvalidVersionError(MetadataError):
    def __init__(self):
        self.value = "Invalid metadata version file"

class MetadataWrongFileFormat(MetadataError):
    def __init__(self):
        self.value = "Invalid metadata version file"
