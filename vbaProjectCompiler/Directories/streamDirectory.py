import os
from vbaProjectCompiler.Directories.directory import Directory

class StreamDirectory(Directory):
    
    def __init__(self):
        super(StreamDirectory, self).__init__()
        self.type = 2
        # Binary Performance Cache data
        self._performanceCache = b''

        # How many bytes does this item reserve in the file.
        # This includes padding to fill a sector or ministream.
        self.bytesUsed = 0

    def getData(self):
        return self.module.getData()

    def setBytesReserved(self, quantity):
        self.bytesUsed = quantity

    def fileSize(self):
        """
        Size in bytes of the compressed file and performance cache
        """
        return self.module.getSize()

    def minifatSectorsUsed(self):
        return (self.fileSize() - 1) // 64 + 1

    @classmethod
    def createFromModule(cls, module):
        ins = cls()
        ins.name = module.modName.value
        ins.module = module
        return ins
