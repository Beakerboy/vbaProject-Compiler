import os
from vbaProjectCompiler.Directories.directory import Directory

class StreamDirectory(Directory):
    type = 2
    filePath = ""

    def fileSize(self):
        if self.filePath == "":
            return 0
        file_size = os.stat(self.filePath)
        return file_size.st_size

    def minifatSectorsUsed(self):
        Return (self.fileSize - 1) // 64 + 1
