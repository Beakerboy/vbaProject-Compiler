import os
from vbaProjectCompiler.Directories.directory import Directory

class StreamDirectory(Directory):
    type = 2
    
    def __init__(self):
        super(StreamDirectory, self).__init__()
        filePath = ""
     

    def fileSize(self):
        """
        Size in bytes of the file after it has been compressed
        """
        if self.filePath == "":
            return 0
        file_size = os.stat(self.filePath)
        return file_size.st_size

    def minifatSectorsUsed(self):
        return (self.fileSize() - 1) // 64 + 1
