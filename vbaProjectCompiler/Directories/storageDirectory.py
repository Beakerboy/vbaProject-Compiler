from vbaProjectCompiler.Directories.directory import Directory

class StorageDirectory(Directory):
    type = 1
    directories = []

    def fileSize(self):
        return 0

    def minifatSectorsUsed(self):
        #Nesd to use the value from the header
        minifatSectorSize = 64
        size = 0
        for dir in directories:
            size += minifatSectorsUsed()
        return size
