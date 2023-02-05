from vbaProjectCompiler.Directories.directory import Directory
from vbaProjectCompiler.Directories.storageDirectory import StorageDirectory


class RootDirectory(StorageDirectory):

    def __init__(self):
        super(RootDirectory, self).__init__()
        self.name = "Root Entry"
        self.type = 5
        VBADirectory = StorageDirectory()
        VBADirectory.name = "VBA"
        self.directories.append(VBADirectory)

    def fileSize(self):
        """
        Need to see how to handle streams that are mixed
        between fat and minifat storage.
        """
        # Need to use the value from the header
        minifatSectorSize = 64
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size * minifatSectorSize

    def addModule(self, module):
        self.directories[0].addModule(module)
        
    def addFile(self, stream):
        self.directories[0].addFile(stream)
