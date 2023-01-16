from vbaProjectCompiler.Directories.directory import Directory

class RootDirectory(Directory):
    type = 5

    directories = []

    def fileSize(self):
        #Nesd to use the value from the header
        minifatSectorSize = 64
        size = 0
        for dir in self.directories:
            size += dir.minifatSectorsUsed()
        return size * minifatSectorSize
       
