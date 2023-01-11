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

        #sectFat = getFirst109FatSectors()
        #header += sectFat
        return header

    def addSreamSectorList(self, list):
        self.streamSectors += list

    def writeFat(i):
        return 1

    def countFatChainSectors(self):
        """Calculate the number of sectors needed to express the FAT chain."""
        #return self.getFatChainLength() / 512 + 1 #intdiv, roundup.
        return 1

    def getFirstDirectoryChainSector(self):
        return 1

    def getDirectoryChainLength(self):
        return 1

    def countMiniFatChainSectors(self):
        return 1
  
    def getFirstMiniChainSector(self):
        return 2
  
    def getFirst109FatSectors(self):
        #return an array of 109 4-byte numbers 
        #00000000 followed by FFFFFFFF 108 times
        return "00000000";

    def writeFatSector(self, i):
        """return a 512 byte sector"""
        return "FE FF FF FF"
        # followed by 511 bytes

    def getFatChainLength(self):
        total = 0
        #get the length of the fat chain including termination and beginning codes
        #Total = getDirectoryChainLength() + 1
        #Total += getMiniFatChainLength() + 1
        #for stream in streams:
        #  total += stream.getChainLength() + 1
        #total += total % 511 #add one double for each sector
        return total
