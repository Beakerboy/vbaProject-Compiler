import struct

from Directory import Directory

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
    uMinorVersion            = 62
    uDllVersion              = 3
    uByteOrder               = "<"
    uSectorShift             = 9
    uMiniSectorShift         = 6
    firstDirectoryListSector = 1
    firstMiniChainSector     = 2
    ulMiniSectorCutoff       = 4096

    
    path = "."  #path to the project root

    #A list of sectors that contain FAT chain information.
    fatSectors = []

    #A list of directories
    directories = []

    #class default constructor
    def __init__(self, path): 
        fatSectors = [0]
        self.path = path
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

    #Getters and Setters
    def getFirstDirectoryListSector(self):
        return self.firstDirectoryListSector

    def setFirstDirectoryListSector(self, i):
        #need to ensure sector is not already reserved
        self.firstDirectoryListSector = i

    def getFirstMiniChainSector(self):
        return self.firstMiniChainSector

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

        csectMiniFat =  self.countMiniFatChainSectors()
        header += struct.pack(self.uByteOrder + "I", csectMiniFat)

        #if the MSAT is longer then 109 entries, it continues at this sector
        sectDifStart = b"\xfe\xff\xff\xff"
        header += sectDifStart

        #if MSAT is longer then 109 entries, here is how many additional sectors of data exist
        csectDif = LONG_ZERO
        header += csectDif

        sectFat = self.writeFatSectorList()
        header += sectFat
        return header

    def writeFat(i):
        return 1

    def countFatChainSectors(self):
        """Calculate the number of sectors needed to express the FAT chain."""
        return self.getFatChainLength() // 511 + 1

    def countDirectoryListSectors(self):
        """The number of sectors needed to express the directory list"""
        # what if the sectors are not 512 bytes?
        directorySectors = (len(self.Directories) - 1) // 4
        return directorySectors

    def countMiniFatChainSectors(self):
        return 1
  
    def writeFatSectorList(self):
        """Create a 436 byte stream of the first 109 FAT sectors, padded with \\xFF"""
        #if the list is longer then 109 entries, need to mange the extended MSAT sectors.
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
