import struct
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory

class DirStream(StreamDirectory):
    """
    The dir stream is compressed on write
    """

    def __init__(self):
        syskind = SimpleRecord(1, 4, 3) #0=16bit, 1=32bit, 2=mac, 3=64bit
        compatVersion = SimpleRecord(74, 4, 3)
        lcid = SimpleRecord(2, 4, 0x0409)
        lcidInvoke = SimpleRecord(12, 4, 0x0409)
        codePage = SimpleRecord(3, 2, 0x04E4)
        projectName = SimpleRecord(4, 10, "VBAProject")
        self.information = [
            syskind,
            compatVersion,
            lcid,
            lcidInvoke,
            codePage,
            projectName
        ]
        self.references  = []
        self.modules = []

    def toBytes(self):
        output = b''
        for record in self.information:
            output += record.pack()
        return output

class SimpleRecord():
    def __init__(self, id, size, value):
        self.id = id
        self.size = size
        self.value = value

    def toDict(self):
        return {"id": self.id, "size": self.size, "value": self.value}

    def pack(self):
        format = "<HI"
        if isinstance(self.value, str):
            format += self.size + "s"
        elif self.size == 2:
            format += "H"
        elif self.size == 4:
            format += "I"
        return struct.pack(format, self.id, self.size, self.value)
