import struct, os
from vbaProjectCompiler.directory import Directory

class VbaProject:

    #data members of class
    uMinorVersion            = 62
    uDllVersion              = 3
    uByteOrder               = "<"
    uSectorShift             = 9
    uMiniSectorShift         = 6
    firstDirectoryListSector = 1
    firstMiniChainSector     = 2
    ulMiniSectorCutoff       = 4096

    #A list of directories
    directories = []

    #the FAT chain
    fatChain = []

    #class default constructor
    # this class probably does not need to be aware of its path. It can just output chunks to a sysio handler.
    def __init__(self):
        #If either self.firstMiniChainSector or self.firstDirectoryListSector is greater then 2, this will be incorrect.
        self.fatChain = [-2, -2]

        root = Directory()
        root.name = "Root Entry"
        root.type = 5
        root.subDirectoryId = 8
        root.modifiedHigh = 3266847680
        root.modifiedLow  =   31007795
        root.sector = 3
        root.size = 6528
        self.directories.append(root)

        vba = Directory()
        vba.name = "VBA"
        vba.type = 1
        vba.subDirectoryId = 4
        vba.modifiedHigh = 3266847680
        vba.modifiedLow  =   31007795
        self.directories.append(vba)

        

    #Getters and Setters
    def getFirstDirectoryListSector(self):
        return self.firstDirectoryListSector

    def setFirstDirectoryListSector(self, i):
        #need to ensure sector is not already reserved
        self.firstDirectoryListSector = i

    def getFirstMiniChainSector(self):
        return self.firstMiniChainSector

    def header(self):
        """Create a 512 byte header sector for a OLE object."""
   
        SHORT_ZERO = b'\x00\x00'
        LONG_ZERO = b'\x00\x00\x00\x00'
        LONG_LONG_ZERO = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
        header = bytearray(absig)

        clsid = LONG_LONG_ZERO + LONG_LONG_ZERO
        header += clsid

        header += struct.pack(self.uByteOrder + "h", self.uMinorVersion)
        header += struct.pack(self.uByteOrder + "h", self.uDllVersion)
        header += struct.pack(self.uByteOrder + "h", -2)
        header += struct.pack(self.uByteOrder + "h", self.uSectorShift)
        header += struct.pack(self.uByteOrder + "h", self.uMiniSectorShift)

        usReserved  = SHORT_ZERO
        header += usReserved

        ulReserved1 = LONG_ZERO
        header += ulReserved1

        csectDir = LONG_ZERO
        header += csectDir

        csectFat = self.countFatChainSectors()
        header += struct.pack(self.uByteOrder + "I",  csectFat)

        sectDirStart =  self.firstDirectoryListSector
        header += struct.pack(self.uByteOrder + "I", sectDirStart)

        signature = LONG_ZERO
        header += signature
        header += struct.pack(self.uByteOrder + "I", self.ulMiniSectorCutoff)

        sectMiniFatStart = self.getFirstMiniChainSector()
        header += struct.pack(self.uByteOrder + "I", sectMiniFatStart)

        csectMiniFat =  self.countMinifatFatChainSectors()
        header += struct.pack(self.uByteOrder + "I", csectMiniFat)

        #if the MSAT is longer then 109 entries, it continues at this sector
        sectDifStart = b"\xfe\xff\xff\xff"
        header += sectDifStart

        #if MSAT is longer then 109 entries, here is how many additional sectors of data exist
        csectDif = LONG_ZERO
        header += csectDif

        sectFat = self.writeHeaderFatSectorList()
        header += sectFat
        return header

    def writeFat(i):
        return 1

    def countFatChainSectors(self):
        """Calculate the number of sectors needed to express the FAT chain."""
        return (len(self.fatChain) - 1) // (2 ** self.uSectorShift - 1) + 1

    def countDirectoryListSectors(self):
        """The number of sectors needed to express the directory list"""
        #Each directory record is 128 bytes
        directoriesPerSector = (2 ** self.uSectorShift) // 128
        directorySectors = (len(self.directories) - 1) // directoriesPerSector + 1
        return directorySectors

    def countMinifatFatChainSectors(self):
        return 1
  
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

    def addFile(self, dir):
        #If a new directory list sector is needed, reserve it in the FAT chain
        #If a new minifat sector is needed, reserve it in the fat chain
        #calulate the start sector
        #update the size of the root sector
        #self.directories[0].size = {count the number of minifat chain entries} * {minifat sector size}
        
        self.directories.append(dir)
    
    def getMinifatChain(self):
        """Use the info in the directory list to create the minifat chain"""
        #foreach element in the array, if the size is greater then zero determine how many 64byte sectors are needed to contain the data
        chain = []
        #All files with data require one sector, how many more are needed.
        additionalMinifatSectors = 0
        for file in self.directories:
            if file.size > 0:
                additionalMinifatSectors = (file.size - 1) // (2 ** self.uMiniSectorShift)
                for i in range(additionalMinifatSectors):
                    chain.append(len(chain) + 1)
                #Append the chain terminator
                chain.append(-2)
        return chain

    def finalize(self):
        #add these if they are missing.
        thisWorkbook = Directory()
        thisWorkbook.name = "ThisWorkbook"
        thisWorkbook.type = 2
        thisWorkbook.color = 1
        thisWorkbook.nextDirectoryId = 5
        thisWorkbook.size = 999
        self.directories.append(thisWorkbook)

        sheet1 = Directory()
        sheet1.name = "Sheet1"
        sheet1.type = 2
        sheet1.color = 1
        sheet1.previousDirectoryId = 6
        sheet1.sector = 16
        sheet1.size = 991
        self.directories.append(sheet1)

        module1 = Directory()
        module1.name = "Module1"
        module1.type = 2
        module1.color = 1
        module1.previousDirectoryId = 3
        module1.nextDirectoryId = 2
        module1.sector = 2
        module1.size = 681
        self.directories.append(module1)

        #these all need to be added
        vba_project = Directory()
        vba_project.name = "_VBA_Project"
        vba_project.type = 2
        vba_project.sector = 43
        vba_project.size = 2544
        self.directories.append(vba_project)

        dir = Directory()
        dir.name = "dir"
        dir.type = 2
        dir.sector = 83
        dir.size = 562
        self.directories.append(dir)

        #This one is not always required.
        projectWm = Directory()
        projectWm.name = "PROJECTwm"
        projectWm.type = 2
        projectWm.sector = 92
        projectWm.size = 86
        self.directories.append(projectWm)

        project = Directory()
        project.name = "PROJECT"
        project.type = 2
        project.color = 1
        project.previousDirectoryId = 1
        project.nextDirectoryId = 7
        project.sector = 94
        project.size = 466
