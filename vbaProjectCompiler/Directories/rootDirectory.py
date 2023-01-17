from vbaProjectCompiler.Directories.directory import Directory
from vbaProjectCompiler.Directories.storageDirectory import StorageDirectory
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory

class RootDirectory(Directory):
    type = 5

    def __init__(self):
        self.directories = []
        self.name = "Root Entry"
        vba_project = StorageDirectory()
        vba_project.name = "VBA"
        super(RootDirectory, self).__init__()
        self.directories.append(vba_project)

        dir_stream = StreamDirectory()
        dir_stream.name = "dir"
        self.directories.append(dir)

    def fileSize(self):
        #Nesd to use the value from the header
        minifatSectorSize = 64
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size * minifatSectorSize

    def addFile(self, stream):
        self.directories[0].addFile(stream)
       
