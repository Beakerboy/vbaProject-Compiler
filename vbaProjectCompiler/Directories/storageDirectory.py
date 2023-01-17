from vbaProjectCompiler.Directories.directory import Directory

class StorageDirectory(Directory):
    type = 1

    def __init__(self):
        directories = []
        super(StorageDirectory, self).__init__()

    def fileSize(self):
        return 0

    def minifatSectorsUsed(self):
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size

    def addFile(self, stream):
        self.directories.append(stream)
