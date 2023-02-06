import struct


class Directory:
    """An OLE directory object"""

    def __init__(self):
        self.name = ""

        self.color = 0

        self.previousDirectoryId = 0xFFFFFFFF
        self.nextDirectoryId = 0xFFFFFFFF
        self.subDirectoryId = 0xFFFFFFFF

        self.classId = ""

        self.userFlags = 0

        self.created = 0
        self.modified = 0

        # The sector where this stream begins
        # This can either be a minifat sector number or a Fat sector
        # depending on the stream size.
        self._startSector = 0
        self.type = 0

    def setStartSector(self, value):
        self._startSector = value

    def getStartSector(self):
        return self._startSector

    def nameSize(self):
        """The byte length of the name"""
        return (len(self.name) + 1) * 2

    def setAdditionalSectors(self, sectorList):
        self._additionalSectors = sectorList

    def fileSize(self):
        return 0

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
            endienSymbol + "IQQIII",
            self.userFlags,
            self.created,
            self.modified,
            self._startSector,
            self.fileSize(),
            0
        )        
        return dir
