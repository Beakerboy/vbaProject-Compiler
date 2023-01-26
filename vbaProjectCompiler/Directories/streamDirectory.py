import os
from vbaProjectCompiler.Directories.directory import Directory

class StreamDirectory(Directory):
    type = 2
    
    def __init__(self):
        super(StreamDirectory, self).__init__()
        self.filePath = ""

        #Binary Performance Cache data
        self._performanceCache = b''

        #How many bytes does this item reserve in the file.
        #This includes padding to fill a sector or ministream.
        self.bytesUsed = 0

    def setPerformanceCache(self, cache):
        self._performanceCache = cache

    def setBytesReserved(self, quantity):
        self.bytesUsed = quantity

    def fileSize(self):
        """
        Size in bytes of the file after it has been compressed
        """
        if self.filePath == "":
            return 0
        file_size = os.stat(self.filePath)
        return file_size.st_size

    def minifatSectorsUsed(self):
        return (self.fileSize() - 1) // 64 + 1

    @classmethod
    def createFromModule(cls, module):
        cls.name = module.name
        return cls
