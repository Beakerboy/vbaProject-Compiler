import struct, os

class OleFile:

    #class default constructor
    def __init__(self, project):
        #Instance Attributes
        self.uMinorVersion            = 62
        self.uDllVersion              = 3
        self.uByteOrder               = "<"
        self.uSectorShift             = 9
        self.uMiniSectorShift         = 6
        self.firstDirectoryListSector = 1
        self.firstMiniChainSector     = 2
        self.ulMiniSectorCutoff       = 4096

        #the FAT chain
        self.fatChain = [65534, 65534]

        #The list of pointers to the address of the next file piece
        minifatChain = []

    def getFirstDirectoryListSector(self):
        return self.firstDirectoryListSector

    def setFirstDirectoryListSector(self, i):
        #need to ensure sector is not already reserved
        self.firstDirectoryListSector = i

    def getFirstMiniChainSector(self):
        return self.firstMiniChainSector

    def header(self):
        """Create a 512 byte header sector for a OLE object."""
   
        LONG_LONG_ZERO = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

        format = self.uByteOrder + "8s16s6H10I"
        header = struct.pack(
            format,
            absig,
            LONG_LONG_ZERO + LONG_LONG_ZERO,  #clsid
            self.uMinorVersion,
            self.uDllVersion,
            65534,   #BOM
            self.uSectorShift,
            self.uMiniSectorShift,
            0,    #usReserved
            0,    #ulReserved1
            0,    #csectDir
            self.countFatChainSectors(),
            self.firstDirectoryListSector,
            0,    #signature
            self.ulMiniSectorCutoff,
            self.getFirstMiniChainSector(),
            self.countMinifatFatChainSectors(),
            self.getDifStartSector(),
            self.countDifSectors()
        )

        sectFat = self.writeHeaderFatSectorList()
        header += sectFat
        return header

    def getDifStartSector(self):
        """
        The Fat sector lost in the header can only list the position of 109 sectors.
        If more sectors are needed, the DIF sector lists these sector numbers.
        """
        if len(self.getFatSectors()) <= 109:
            return 65534
        #research how Dif works
        return 0

    def countDifSectors(self):
        """
        How many sectors of 512 entries are needed to list the positions of the remaining FAT sectors
        What is sectors are not 512 bytes?
        """
        count = self.countFatChainSectors()
        if count <= 109:
            return 0
        return (count - 109 - 1) // (2 ** (self.uSectorShift - 2)) + 1

    def countFatChainSectors(self):
        """
        Calculate the number of sectors needed to express the FAT chain.
        """
        return (len(self.fatChain) - 1) // (2 ** self.uSectorShift - 1) + 1

    def countDirectoryListSectors(self):
        """
        The number of sectors needed to express the directory list
        """
        #Each directory record is 128 bytes
        directoriesPerSector = (2 ** self.uSectorShift) // 128
        directorySectors = (len(self.directories) - 1) // directoriesPerSector + 1
        return directorySectors

    def countMinifatFatChainSectors(self):
        addressesPerSector = 2 ** (self.uSectorShift - 2)
        return max((len(self.minifatChain) - 1) // addressesPerSector + 1, 1)
  
    def writeHeaderFatSectorList(self):
        """Create a 436 byte stream of the first 109 FAT sectors, padded with \\xFF"""
        #if the list is longer then 109 entries, need to mange the extended MSAT sectors.
        output = b''
        list = self.getFatSectors()
        for sector in list[0:109]:
            output += struct.pack(self.uByteOrder + "I", sector)
        output = output.ljust(436, b'\xff')
        return output

    def getFatSectors(self):
        """List which sectors contain FAT chain information. They should be on 128 sector intervals."""
        sectorList = []
        numberOfSectors = self.countFatChainSectors()
        for i in range(numberOfSectors):
            sectorList.append(i * (2 ** (self.uSectorShift - 2)))
        return sectorList

    def writeFatSector(self, i):
        """return a 512 byte sector"""
        return "FE FF FF FF"
        # followed by 511 bytes

    def getFatChainLength(self):
        """Count the number of entries in the complete FAT chain."""
        total = ((len(self.fatChain) - 1) // (2 ** self.uSectorShift - 1) + 1) * (2 ** self.uSectorShift)
        return total
