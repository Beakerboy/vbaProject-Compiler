import struct, os
from vbaProjectCompiler.Directories.directory import Directory

class OleFile:

   
    #class default constructor
    def __init__(self, project):
        self.HEADER_BYTES = 512
        self.project = project

        #Instance Attributes
        self.uMinorVersion            = 62
        self.uDllVersion              = 3
        self.uSectorShift             = 9
        self.uMiniSectorShift         = 6
        self.firstDirectoryListSector = 1
        self.firstMiniChainSector     = 2
        self.ulMiniSectorCutoff       = 4096

        #the FAT chain starts at sector zero, so element zero marks this sector as a fat sector.
        self.fatChain = [0xfffffffd]

        #The list of pointers to the address of the next file piece
        self.minifatChain = []

        #A list of directories
        self.directories = []

        self.createInitialDirectories()

    def getFirstDirectoryListSector(self):
        return self.firstDirectoryListSector

    def setFirstDirectoryListSector(self, i):
        #need to ensure sector is not already reserved
        self.firstDirectoryListSector = i

    def getFirstMiniChainSector(self):
        return self.firstMiniChainSector

    def createInitialDirectories(self):
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

    def header(self):
        """Create a 512 byte header sector for a OLE object."""
        packSymbol = '<' if self.project.endien == 'little' else '>'
        LONG_LONG_ZERO = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

        format = packSymbol + "8s16s6H10I"
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
            return 0xfffffffe
        #research how Dif works
        return 0

    def countDifSectors(self):
        """
        How many sectors of 512 entries are needed to list the positions of the remaining FAT sectors
        What if sectors are not 512 bytes?
        """
        count = self.countFatChainSectors()
        if count <= 109:
            return 0
        return (count - 109 - 1) // (2 ** (self.uSectorShift - 2)) + 1

    def countFatChainSectors(self):
        """
        Calculate the number of sectors needed to express the FAT chain.
        """
        return max((len(self.fatChain) - 1) // (2 ** self.uSectorShift - 1) + 1, 1)

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
        """
        Create a 436 byte stream of the first 109 FAT sectors, padded with \\xFF
        """
        packSymbol = '<' if self.project.endien == 'little' else '>'
        #if the list is longer then 109 entries, need to mange the extended MSAT sectors.
        output = b''
        list = self.getFatSectors()
        for sector in list[0:109]:
            output += struct.pack(packSymbol + "I", sector)
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
        """
        Write a full sector's worth of FAT chain data.
        Zero indexed
        """
        #Each address is 4 bytes 
        addressesPerSector = 2 ** (self.uSectorShift - 2)
        start = i * addressesPerSector
        end = (i + 1) * addressesPerSector
        sectors = self.fatChain[start:end]
        output = b''
        packSymbol = '<' if self.project.endien == 'little' else '>'
        format = packSymbol + "I"
        for sector in sectors:
            output += struct.pack(format, sector)
        #Pad the output to fill the sector.
        output = output.ljust(2 ** self.uSectorShift, b'\xff')
        return output

    def getMinifatChain(self):
        """
        Use the info in the directory list to create the minifat chain
        """
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

    def bytesPerSector(self):
        return 2 ** self.uSectorShift

    def bytesPerMinifatSector(self):
         return 2 ** self.uMiniSectorShift

    def findMinifatSectorOffset(self, sectorNumber):
        """
        Get the file offset for a specific minifat sector number
        Zero Indexed
        """
        MinifatSectorsPerSector = 2 ** (self.uSectorShift - self.uMiniSectorShift)
        fatChainDepth = sectorNumber // MinifatSectorsPerSector
        remainingMinifatSectors = sectorNumber % MinifatSectorsPerSector
        return self.findFileOffset(self.firstMiniChainSector, fatChainDepth) + remainingMinifatSectors * self.bytesPerMinifatSector()

    def findFileOffset(self, startSector, depth):
        """
        Follow the fat chain starting at startSector, for depth hops to find the file offset.
        depth is zero or greater.
        """
        sector = startSector
        for i in range(depth):
            sector = self.fatChain[sector]
        return sector * self.bytesPerSector() + 512

    def finalize(self):
        #add these if they are missing.
        thisWorkbook = Directory()
        thisWorkbook.name = "ThisWorkbook"
        thisWorkbook.type = 2
        thisWorkbook.color = 1
        thisWorkbook.nextDirectoryId = 5
        thisWorkbook.size = 999
        #self.directories.append(thisWorkbook)

        sheet1 = Directory()
        sheet1.name = "Sheet1"
        sheet1.type = 2
        sheet1.color = 1
        sheet1.previousDirectoryId = 6
        sheet1.sector = 16
        sheet1.size = 991
        #self.directories.append(sheet1)

        module1 = Directory()
        module1.name = "Module1"
        module1.type = 2
        module1.color = 1
        module1.previousDirectoryId = 3
        module1.nextDirectoryId = 2
        module1.sector = 2
        module1.size = 681
        #self.directories.append(module1)

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

    def writeFile(self, path):
        """
        Write the OLE file
        """
        packSymbol = '<' if self.project.endien == 'little' else '>'
        f = open(path + '/vbaProject.bin', 'wb+')
        f.write(self.header())
        #write an empty Fat sector
        f.write(self.writeFatSector(0))
        ##write empty directory sector
        f.seek(self.HEADER_BYTES + self.firstDirectoryListSector * 4)
        f.write(struct.pack(packSymbol + 'I', 0xfffffffe))
        f.seek(self.HEADER_BYTES + self.firstDirectoryListSector * self.bytesPerSector())
        #f.write()
        ##write empty minifat sector
        ##pull data from self.project
        #for module in self.project.modules:
            # add each as a directory listing
        # add _VBA_Project
        # add dir
        # add projectWm
        # add project
        #Get the first sector of directories
        i = 0
        entriesPerSector = self.uSectorShift - 3 + 1
        start = i * entriesPerSector
        end = (i + 1)* entriesPerSector
        entries = self.directories[start:end]
        #initialize sector with zeroes.
        for directory in entries:
            if directory.type != 2:
                #write directory object
                pass
            elif directory.size > self.ulMiniSectorCutoff:
    
                #find first unused fat sector
                # save starting sector to object
                # write directory entry
                # initialize sectors with zeros
                # update fat chain
                # write data
                pass
            else:
                #Find the first unused minifat location
                # save starting sector to object
                # write directory entry
                # determine for many minifat sectors are needed
                # determine if a new minifat sector chain is needed
                    #write a new sector
                    # update fat chain
                # determine if a new data sector is needed
                    #update fat chain
                    #initialize
                # overwrite minifat sectors with data
                pass
