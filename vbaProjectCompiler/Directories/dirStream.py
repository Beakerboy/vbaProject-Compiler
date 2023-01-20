import struct
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory

class DirStream(StreamDirectory):
    """
    The dir stream is compressed on write
    """

    def __init__(self):
        self.codePage = 0x04E4
        codePageName = "cp" + str(self.codePage)
        syskind = SimpleRecord(1, 4, 3) #0=16bit, 1=32bit, 2=mac, 3=64bit
        compatVersion = SimpleRecord(74, 4, 3)
        lcid = SimpleRecord(2, 4, 0x0409)
        lcidInvoke = SimpleRecord(20, 4, 0x0409)
        codePageRecord = SimpleRecord(3, 2, self.codePage)
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
            codePageRecord,
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
       
        refName1 = SimpleRecord(0x0016, 6, refString.encode(codePageName))
        refName2 = SimpleRecord(0x003E, 12, refString.encode("utf_16_le"))
        libidRef = LibidReference(
            "windows",
            "{00020430-0000-0000-C000-000000000046}",
            "2.0",
            "0",
            "C:\\Windows\\System32\\stdole2.tlb",
            "OLE Automation"
        )
        refRegistered = PackedRecord(struct.pack("<III94sIH",0x000D, 0x0068, 0x005E, libidRef.toString().encode(codePageName), 0, 0))
       
        self.references  = [
            refName1,
            refName2,
            refRegistered
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
    """
    Many Records in this class have the same format, a two bye ID, a four byte size and an int value formatted to the defined si
    """

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

class PackedRecord():
    """
    A Record that is already packed
    """
    def __init__(self, value):
        self.value = value

    def pack(self):
        return self.value

class LibidReference():
    def __init__(pathType, libidGuid, version, libidLcid, libidPath, libidRegName)
        self.LibidReferenceKind = "G" if pathType = "windows" else "H"
        self.libidGuid = libidGuid
        self.version = version
        self.libidPath = libidPath
        self.libidRegName = libidRegName

    toString():
        return "*\\" +
            self.LibidReferenceKind +
            self.libidGuid + "#" +
            self.version + "#" +
            self.libidPath + "#" +
            self.libidRegName
     

            
