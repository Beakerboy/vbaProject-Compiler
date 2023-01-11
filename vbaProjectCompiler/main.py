import struct

def main(args):
    return 1

def writeFile():
    writeHeader()
    writeFat(0)
    
    # second fat block is 80000000

def writeHeader():
    """Create a 512 byte header sector for a OLE object."""
   
    SHORT_ZERO = "\x00\x00"
    LONG_ZERO = SHORT_ZERO + SHORT_ZERO
    LONG_LONG_ZERO = LONG_ZERO + LONG_ZERO
    header = ""

    absig = "\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
    header += absig

    clsid = LONG_LONG_ZERO + LONG_LONG_ZERO
    header += clsid

    uMinorVersion = "\x3e\x00"
    header += uMinorVersion

    uDllVersion = "\x03\x00"
    header += uDllVersion

    uByteOrder = "\xfe\xff"
    header += uByteOrder

    uSectorShift = "\x09\x00"
    header += uSectorShift

    uMiniSectorShift = "\x06\x00"
    header += uMiniSectorShift

    usReserved  = SHORT_ZERO
    header += usReserved

    ulReserved1 = LONG_ZERO
    header += ulReserved1

    csectDir = LONG_ZERO
    header == csectDir

    csectFat = countFatChainSectors()
    header += struct.pack("<I",  csectFat)

    sectDirStart =  getFirstDirectoryChainSector()
    header += struct.pack("<I", sectDirStart)

    signature = LONG_ZERO
    header += signature

    ulMiniSectorCutoff = "\x00\x10\x00\x00"
    header += ulMiniSectorCutoff

    sectMiniFatStart = getFirstMiniChainSector()
    header += sectMiniFatStart

    csectMiniFat =  countMiniFatChainSectors()
    header += csectMiniFat

    sectDifStart = "\xfe\xff\xff\xff"
    header += sectDifStart

    csectDif = LONG_ZERO
    header += csectDif

    sectFat = getFirst109FatSectors()
    header += sectFat
    return header

def writeFat(i):
    return 1

def countFatChainSectors():
    """Calculate the number of sectors needed to express the FAT chain."""
    #return getFatChainLength() / 512 + 1 #intdiv, roundup.
    return 1

def getFirstDirectoryChainSector():
    return 1

def getDirectoryChainLength():
    return 1

def countMiniFatChainSectors():
    return 1
  
def getFirstMiniChainSector():
    return 2
  
def getFirst109FatSectors():
    #return an array of 109 4-byte numbers 
    #00000000 followed by FFFFFFFF 108 times
    return "00000000";

def writeFatSector(i):
    """return a 512 byte sector"""
    return "FE FF FF FF"
    # followed by 511 bytes

def getFatChainLength():
    total = 0
    #get the length of the fat chain including termination and beginning codes
    #Total = getDirectoryChainLength() + 1
    #Total += getMiniFatChainLength() + 1
    #for stream in streams:
    #  total += stream.getChainLength() + 1
    #total += total % 511 #add one double for each sector
    return total
