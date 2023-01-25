import struct, os
from vbaProjectCompiler.Directories.directory import Directory

class VbaProject:

    #class default constructor
    def __init__(self):

        self.endien = 'little'

        # Protected Instance Attributes
        self._codePageName = 'cp1252'
        self._projectId = '{}'
        self._protectionState = "0705D8E3D8EDDBF1DBF1DBF1DBF1"
        self._password = "0E0CD1ECDFF4E7F5E7F5E7"
        self._visibilityState = "1517CAF1D6F9D7F9D706"
        self._performanceCache = b''
        self._performanceCacheVersion = 0xFFFF

        #A list of directories
        self.directories = []
        self.references  = []
        self.modules     = []

        self.projectCookie = 0xFFFF
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
    def setProjectId(self, id):
        self._projectId = id

    def getProjectId(self):
        return self._projectId

    def setProtectionState(self, state):
        self._protectionState = state

    def getProtectionState(self):
        return self._protectionState

    def setVisibilityState(self, state):
        self._visibilityState = state

    def getVisibilityState(self):
        return self._visibilityState

    def setPassword(self, value):
        self._password = value

    def getPassword(self):
        return self._password

    def setPerformanceCache(self, cache):
        self._performanceCache = cache

    def getPerformanceCache(self):
        return self._performanceCache

    def setPerformanceCacheVersion(self, version):
        self._performanceCacheVersion = version

    def getPerformanceCacheVersion(self):
        return self._performanceCacheVersion

    def getCodePageName(self):
        return self._codePageName

   

    def addFile(self, dir):
        #If a new directory list sector is needed, reserve it in the FAT chain
        #If a new minifat sector is needed, reserve it in the fat chain
        #calulate the start sector
        #update the size of the root sector
        #add data to PROJECT data structure
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

    def addReference(self, ref):
        self.references.append(ref)

    def addModule(self, ref):
        self.modules.append(ref)

    def setProjectCookie(self, value):
        self.projectCookie = value
