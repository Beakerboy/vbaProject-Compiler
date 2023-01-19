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
        lcidInvoke = SimpleRecord(20, 4, 0x0409)
        codePage = SimpleRecord(3, 2, 0x04E4)
        projectName = SimpleRecord(4, 10, "VBAProject")
        #docString = ArrayRecord(5, [0,0], ["", ""], 0x0040)
        docString1 = SimpleRecord(5, 0, "")
        docString2 = SimpleRecord(0x0040, 0, "")
        #helpFile = ArrayRecord(6, [0,0], ["", ""], 0x003D)
        helpContext = SimpleRecord(7, 4, 0)
        libFlags = SimpleRecord(8, 4, 0)
        version = SimpleRecord(9, 4, 0x65BE0257)
        minorVersion = 17
        #constants = ArrayRecord(12,[0, 0],["", ""], 0x003C)
        self.information = [
            syskind,
            compatVersion,
            lcid,
            lcidInvoke,
            codePage,
            projectName,
            docString1,
            docString2
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
            self.stringValue = self.value
            self.value = bytes(self.value, encoding = "ascii")
            format += str(self.size) + "s"
        elif self.size == 2:
            format += "H"
        elif self.size == 4:
            format += "I"
        output = struct.pack(format, self.id, self.size, self.value)
        #clean up stringValue
        return output
