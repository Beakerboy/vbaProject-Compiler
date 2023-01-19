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
        
        docString1 = SimpleRecord(5, 0, "")       #multibute string
        docString2 = SimpleRecord(0x0040, 0, "")  #UTF-16

        helpfile1 = SimpleRecord(6, 0, "")
        helpfile2 = SimpleRecord(0x003D, 0, "")
        helpContext = SimpleRecord(7, 4, 0)
        libFlags = SimpleRecord(8, 4, 0)
        version = SimpleRecord(9, 4, 0x65BE0257)
        minorVersion = SimpleValue(2, 17)
        constants1 = SimpleRecord(12, 0, "")
        constants2 = SimpleRecord(0x003C, 0, "")
        self.information = [
            syskind,
            compatVersion,
            lcid,
            lcidInvoke,
            codePage,
            projectName,
            docString1,
            docString2,
            helpfile1,
            helpfile2,
            helpContext,
            libFlags,
            version,
            minorVersion,
            constants1,
            constants2
        ]
        refString = "stdole"
        refName1 = SimpleRecord(16, 6, refString) #should be encoded using CodePage
        refName2 = SimpleRecord(0x003E, 12, refString.encode("utf-16"))
        self.references  = [
            refName1,
            refName2
        ]
        self.modules = []

    def toBytes(self):
        output = b''
        for record in self.information:
            output += record.pack()
        for record in self.references:
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
        elif isinstance(self.value, bytes):
            format += str(self.size) + "s"
        elif self.size == 2:
            format += "H"
        elif self.size == 4:
            format += "I"
        else:
            raise Exception("Received data of type " + type(self.value).__name__)
        output = struct.pack(format, self.id, self.size, self.value)
        #clean up stringValue
        return output

class SimpleValue():
    def __init__(self, size, value):
        self.size = size
        self.value = value

    def pack(self):
        format = "<"
        if self.size == 2:
            format += "H"
        elif self.size == 4:
            format += "I"
        output = struct.pack(format, self.value)
        return output
