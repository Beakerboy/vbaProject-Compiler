import struct

class Directory:
    """An OLE directory object"""
    
    def __init__(self):
        self.name = ""

        self.color = 0

        self.previousDirectoryId = 0xFFFFFFFF
        self.nextDirectoryId     = 0xFFFFFFFF
        self.subDirectoryId      = 0xFFFFFFFF

        self.classId = ""

        self.userFlags = 0

        self.created  = 0
        self.modifiedHigh = 0
        self.modifiedLow = 0

        self.sector = 0

    def nameSize(self):
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def fileSize(self):
        pass

    def writeDirectory(self, codePageName, endien):
        endienSymbol = '<' if endien == 'little' else '>'
        format = endienSymbol + "64shbb3I"
        
        dir = struct.pack(
            format,
            self.name.encode("utf_16_le"),
            self.nameSize(),
            self.type,
            self.color,
            self.previousDirectoryId,
            self.nextDirectoryId,
            self.subDirectoryId
        )
        dir += bytearray(self.classId, "utf8").ljust(16, b'\x00')
        dir += struct.pack(
            endienSymbol + "IQIIIII",
            self.userFlags,
            self.created,
            self.modifiedHigh,
            self.modifiedLow,
            self.sector,
            self.fileSize(),
            0
        )        
        return dir
