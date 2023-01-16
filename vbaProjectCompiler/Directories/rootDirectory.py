from vbaProjectCompiler.Directories.directory import Directory

class RootDirectory(Directory):
    type = 5

    directories = []

    def fileSize(self):
        #iterate through the directories list
        #if the item is a stream, ask for its size and round
        #up to fill the minifat block.
