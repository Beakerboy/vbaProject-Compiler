import struct, os

class Directory:
    """An OLE directory object"""
    name = ""

    type = 0

    color = 0

    previousDirectoryId = -1
    nextDirectoryId     = -1
    subDirectoryId      = -1

    classId = ""

    userFlags = 0

    created  = 0
    modifiedHigh = 0
    modifiedLow = 0

    sector = 0

    def nameSize(self):
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def fileSize(self):
        pass

    def writeDirectory(self):
        dir = bytearray(self.name, "utf_16_le")
        dir = dir.ljust(64, b'\x00')
        dir += struct.pack("<h", self.nameSize())
        dir += struct.pack("b", self.type)
        dir += struct.pack("b", self.color)
        dir += struct.pack("<i", self.previousDirectoryId)
        dir += struct.pack("<i", self.nextDirectoryId)
        dir += struct.pack("<i", self.subDirectoryId)
        dir += bytearray(self.classId, "utf8").ljust(16, b'\x00')
        dir += struct.pack("<I", self.userFlags)
        dir += struct.pack("<q", self.created)
        dir += struct.pack("<I", self.modifiedHigh)
        dir += struct.pack("<I", self.modifiedLow)
        dir += struct.pack("<I", self.sector)
        dir += struct.pack("<I", self.fileSize())
        dir += struct.pack("<I", 0)
        
        return dir
