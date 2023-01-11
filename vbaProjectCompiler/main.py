import struct

def main(args):
    rootPath = args[1]
    vbaProject = VbaProject(rootPath)
    #for each .bas file in rootPath/Modules
    # compress file
    # add file to the project

    #for each .cls file in rootPath/ClassModules
    # compress file
    # add file to the project

    #for each .frm file in rootPath/Forms
    # compress file
    # add file to the project

    vbaProject.write(rootPath)

class VbaProject:

    #data members of class
    path = "."  #path to the project root

    #Each element is a chain of sector numbers for a particular stream.
    streamSectors = []

    #A list of sectors that contain FAT chain information.
    fatSectors = []

    #A list of directories
    directories = []

    #class default constructor
    def __init__(self, path): 
          self.path = path

    def write(self):
        #open filestream to path.vbaProject.bin
        # write self.header()
        # write self.FatSector(0)
        # write self.directorySector(0)
        # write self.miniFatSector(0)
        # second fat block is 80000000
        return 1

    def header(self):
        """Create a 512 byte header sector for a OLE object."""
   
        SHORT_ZERO = b'\x00\x00'
        LONG_ZERO = b'\x00\x00\x00\x00'
        LONG_LONG_ZERO = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
        header = bytearray(absig)

        clsid = LONG_LONG_ZERO + LONG_LONG_ZERO
        header += clsid

        uMinorVersion = b"\x3e\x00"
        header += uMinorVersion

        uDllVersion = b"\x03\x00"
        header += uDllVersion

        uByteOrder = b"\xfe\xff"
        header += uByteOrder

        uSectorShift = b"\x09\x00"
        header += uSectorShift

        uMiniSectorShift = b'\x06\x00'
        header += uMiniSectorShift

        usReserved  = SHORT_ZERO
        header += usReserved

        ulReserved1 = LONG_ZERO
        header += ulReserved1

        csectDir = LONG_ZERO
        header += csectDir

        csectFat = self.countFatChainSectors()
        header += struct.pack("<I",  csectFat)

        sectDirStart =  self.getFirstDirectoryChainSector()
        header += struct.pack("<I", sectDirStart)

        signature = LONG_ZERO
        header += signature

        ulMiniSectorCutoff = b"\x00\x10\x00\x00"
        header += ulMiniSectorCutoff

        sectMiniFatStart = self.getFirstMiniChainSector()
        header += struct.pack("<I", sectMiniFatStart)

        csectMiniFat =  self.countMiniFatChainSectors()
        header += struct.pack("<I", csectMiniFat)

        sectDifStart = b"\xfe\xff\xff\xff"
        header += sectDifStart

        csectDif = LONG_ZERO
        header += csectDif

        sectFat = self.writeFatSectorList()
        header += sectFat
        return header

    def addStreamSectorList(self, list):
        """Add a list of sector numbers to the FAT table."""
        self.streamSectors.append(list)

    def countStreams(self):
        """Return the number of streams defined in the FAT table."""
        return len(self.streamSectors)

    def writeFat(i):
        return 1

    def countFatChainSectors(self):
        """Calculate the number of sectors needed to express the FAT chain."""
        return self.getFatChainLength() // 511 + 1

    def getFirstDirectoryChainSector(self):
        return 1

    def getDirectoryChainLength(self):
        return 1

    def countMiniFatChainSectors(self):
        return 1
  
    def getFirstMiniChainSector(self):
        return 2
  
    def writeFatSectorList(self):
        """Create a 436 byte stream of the first 109 FAT sectors, padded with \\xFF"""
        list = bytearray(b'\x00\x00\x00\x00')
        if self.countFatChainSectors() > 1:
            #the second FAT sector is number 128.
            pass
        list = list.ljust(436, b'\xff')
        return list

    def getFatSectors(self):
        sectorList = [0]
        # add 
        return sectorList

    def writeFatSector(self, i):
        """return a 512 byte sector"""
        return "FE FF FF FF"
        # followed by 511 bytes

    def getFatChainLength(self):
        """Count the number of entries in the complete FAT chain."""
        total = 1
        for stream in self.streamSectors:
            total += len(stream) + 1
        return total

class Directory:
    """An OLE directory object"""
    name = ""

    type = 0

    color = 0

    previousDirectoryId = -1
    nextDirectoryId     = -1
    subDirectoryId      = -1

    classId = 0

    userFlags = 0

    created  = 0
    modified = 0

    sector = 0

    size = 0

   def nameSize(self):
       """The byte length of the name"""
       return (len(self.name) + 1) * 2

    def writeDirectory(self):
      return 1
