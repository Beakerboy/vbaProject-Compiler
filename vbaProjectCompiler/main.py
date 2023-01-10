def main(args):

def writeHeader():
  
    LONG_ZERO = "0x00000000"
    SHORT_ZERO = "0x0000"
    
    absig = "0xD0CF11E0A1B11AE1"
    clsid = "0x00 00 00 00 00 00 00 0000 00 00 00 00 00 00 00" 
    uMinorVersion = "3E 00"
    uDllVersion = "03 00" 
    uByteOrder = "FE FF"
    uSectorShift = "09 00"
    uMiniSectorShift = "06 00"
    usReserved  = SHORT_ZERO
    ulReserved1 = LONG_ZERO
    csectDir = LONG_ZERO
    csectFat = countFatChainSectors()
    sectDirStart =  getFirstDirectoryChainSector()
    signature = LONG_ZERO
    ulMiniSectorCutoff = "00 10 00 00" 
    sectMiniFatStart = getFirstMiniChainSector()
    csectMiniFat =  countMiniFatChainSectors()
    sectDifStart = "FE FF FF FF"
    csectDif = LONG_ZERO
    sectFat = getFirst109FatSectors()
    
def countFatChainSectors():
    return "0x010000"

def getFirstDirectoryChainSector():
    return "0x010000"

def countMiniFatChainSectors():
    return "0x010000"
  
def getFirstMiniChainSector():
    return "0x020000"
  
def getFirst109FatSectors()
    #return an array of 109 4-byte numbers 
    #00000000 followed by FFFFFFFF 108 times
