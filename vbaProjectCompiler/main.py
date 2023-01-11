def main(args):
    return 1

def writeFile():
    writeHeader()
    writeFat(0)
    
    # second fat block is 80000000

def writeHeader():
    """Create a 512 byte header sector for a OLE object."""
    DOUBLE_ZERO = "0000000000000000"
    LONG_ZERO = "00000000"
    SHORT_ZERO = "0000"
    header = ""

    absig = "D0CF11E0A1B11AE1"
    header += absig

    clsid = DOUBLE_ZERO + DOUBLE_ZERO
    header += clsid

    uMinorVersion = "3E00"
    header += uMinorVersion

    uDllVersion = "0300"
    header += uDllVersion

    uByteOrder = "FEFF"
    header += uByteOrder

    uSectorShift = "0900"
    header += uSectorShift

    uMiniSectorShift = "0600"
    header += uMiniSectorShift

    usReserved  = SHORT_ZERO
    header += usReserved

    ulReserved1 = LONG_ZERO
    header += ulReserved1

    csectDir = LONG_ZERO
    header == csectDir

    csectFat = countFatChainSectors()
    header += csectFat

    sectDirStart =  getFirstDirectoryChainSector()
    header += sectDirStart

    signature = LONG_ZERO
    header += signature

    ulMiniSectorCutoff = "00100000" 
    header += ulMiniSectorCutoff

    sectMiniFatStart = getFirstMiniChainSector()
    header += sectMiniFatStart

    csectMiniFat =  countMiniFatChainSectors()
    header += csectMiniFat

    sectDifStart = "FEFFFFFF"
    header += sectDifStart

    csectDif = LONG_ZERO
    header += csectDif

    sectFat = getFirst109FatSectors()
    header += sectFat

def countFatChainSectors():
    """Calculate the number of sectors needed to express the FAT chain."""
    return getFatChainLength() / 512 + 1 #intdiv, roundup.

def getFirstDirectoryChainSector():
    return 1

def countMiniFatChainSectors():
    return 1
  
def getFirstMiniChainSector():
    return 2
  
def getFirst109FatSectors():
    #return an array of 109 4-byte numbers 
    #00000000 followed by FFFFFFFF 108 times

def writeFatSector(i):
    #return a 512 byte sector
    return FE FF FF FF followed by 511 bytes

def getFatChainLength():
    #get the length of the fat chain including termination and beginning codes
    Total = getDirectoryChainLength() + 1
    Total += getMiniFatChainLength() + 1
    foreach (getStreams as stream)
      total += stream.getChainLength() + 1
    Total += total % 511 #add one double for each sector
    return total

def formatLittleEndien(input, bytes):
    # return a string of the byte representation
    Given formatLittleEndien(1,4) return "01000000"
