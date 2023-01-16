from vbaProjectCompiler.Directories.directory import Directory

class StorageDirectory(Directory):
    type = 1

    def fileSize(self):
        return 0
