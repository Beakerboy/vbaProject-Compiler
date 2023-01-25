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
        self.fatChain = [-2, -2]

        #The list of pointers to the address of the next file piece
        minifatChain = []
