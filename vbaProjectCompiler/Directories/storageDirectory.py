from vbaProjectCompiler.Directories.directory import Directory

class StorageDirectory(Directory):
    type = 1
    directories = []
    def fileSize(self):
        return 0
