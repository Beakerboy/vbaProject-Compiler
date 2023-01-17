from vbaProjectCompiler.Directories.directory import Directory
from vbaProjectCompiler.Directories.storageDirectory import StorageDirectory

class RootDirectory(Directory):
    type = 5

    def __init__(self):
        directories = []
        vba_project = StorageDirectory()
        super(RootDirectory, self).__init__()
        self.directories.append(vba_project)
       

    def fileSize(self):
        #Nesd to use the value from the header
        minifatSectorSize = 64
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size * minifatSectorSize

    def addFile(self, stream):
        self.directories[0].addFile(stream)
       
