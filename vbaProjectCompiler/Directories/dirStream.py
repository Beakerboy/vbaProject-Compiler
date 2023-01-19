from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory

class DirStream(StreamDirectory):
    """
    The dir stream is compressed on write
    """

    def __init__(self):
        self.information = []
        self.references = []
        self.modules = []

    def toBytes(self):
        #return
        #information + references + modules + 0x0010 + 0x00000000
        pass
