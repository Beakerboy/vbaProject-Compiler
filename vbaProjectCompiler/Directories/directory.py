import struct

class Directory:
    """An OLE directory object"""
    
    def __init__(self):
        self.name = ""

        self.color = 0

        self.previousDirectoryId = -1
        self.nextDirectoryId     = -1
        self.subDirectoryId      = -1

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

    def writeDirectory(self):
        format = "<64shbbiii"
        
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
            "<IqIIIII",
            self.userFlags,
            self.created,
            self.modifiedHigh,
            self.modifiedLow,
            self.sector,
            self.fileSize(),
            0
        )        
        return dir
