from vbaProjectCompiler.Directories.directory import Directory

class StorageDirectory(Directory):
    type = 1

    def __init__(self):
        self.directories = []
        super(StorageDirectory, self).__init__()

    def fileSize(self):
        return 0

    def minifatSectorsUsed(self):
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size

    def paddedBytesUsed(self):
        size = 0
        for dir in self.directories:
            size += dir.paddedBytesUsed()
        return size

    def addFile(self, stream):
        self.directories.append(stream)

    def createBinaryTree(self):
        pass

    def flatten(self):
        self.flat = [self]
        for child in self.directories:
            if child.type == 2:
                self.flat.append(child)
            else
                self.flat.append(child.flaten())
        return self.flat
