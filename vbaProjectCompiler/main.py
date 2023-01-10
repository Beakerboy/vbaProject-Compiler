def main(args):

def writeFile():
    writeHeader()
    writeFat(0)
    
    # second fat block is 80000000

def writeHeader():
    DOUBLE_ZERO = "0000000000000000"
    LONG_ZERO = "00000000"
    SHORT_ZERO = "0000"
    
    absig = "D0CF11E0A1B11AE1"
    clsid = DOUBLE_ZERO + DOUBLE_ZERO
    uMinorVersion = "3E00"
    uDllVersion = "0300" 
    uByteOrder = "FEFF"
    uSectorShift = "0900"
    uMiniSectorShift = "0600"
    usReserved  = SHORT_ZERO
    ulReserved1 = LONG_ZERO
    csectDir = LONG_ZERO
    csectFat = countFatChainSectors()
    sectDirStart =  getFirstDirectoryChainSector()
    signature = LONG_ZERO
    ulMiniSectorCutoff = "00100000" 
    sectMiniFatStart = getFirstMiniChainSector()
    csectMiniFat =  countMiniFatChainSectors()
    sectDifStart = "FEFFFFFF"
    csectDif = LONG_ZERO
    sectFat = getFirst109FatSectors()
    
def countFatChainSectors():
    return getFatChainLength() / 512 + 1 #intdiv, roundup.

def getFirstDirectoryChainSector():
    return "01000000"

def countMiniFatChainSectors():
    return "0x01 00 00 00"
  
def getFirstMiniChainSector():
    return "0x02 00 00 00"
  
def getFirst109FatSectors()
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
