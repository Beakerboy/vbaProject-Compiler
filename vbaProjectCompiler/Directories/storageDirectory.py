from vbaProjectCompiler.Directories.directory import Directory

class StorageDirectory(Directory):
    type = 1
    directories = []

    def fileSize(self):
        return 0

    def minifatSectorsUsed(self):
        size = 0
        for dir in directories:
            size += minifatSectorsUsed()
        return size
