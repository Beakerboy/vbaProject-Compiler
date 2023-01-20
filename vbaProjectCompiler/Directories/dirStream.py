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
        libidRef = LibidReference(
            "windows",
            "{00020430-0000-0000-C000-000000000046}",
            "2.0",
            "0",
            "C:\\Windows\\System32\\stdole2.tlb",
            "OLE Automation"
        )
        oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
        libidRef2 = LibidReference(
            "windows",
            "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
            "2.0",
            "0",
            "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
            "Microsoft Office 16.0 Object Library"
        )
        officeReference = ReferenceRecord(codePageName, "Office", libidRef2)
        self.references  = [
            oleReference,
            officeReference
        ]
        cookie = SimpleRecord(19, 2, 0x08F3) #should be 0xFFFF
        count = 3
        modulesHeader = SimpleRecord(0x000F, 2, count)
        thisWorkbook = ModuleRecord(codePageName, "ThisWorkbook", "ThisWorkbook", "", 0x0333, 0, 0xB81C, 0x0022)
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
    def __init__(self, pathType, libidGuid, version, libidLcid, libidPath, libidRegName):
        self.LibidReferenceKind = "G" if pathType == "windows" else "H"
        self.libidGuid = libidGuid
        self.version = version
        self.libidLcid = libidLcid
        self.libidPath = libidPath
        self.libidRegName = libidRegName

    def toString(self):
        return "*\\" + \
            self.LibidReferenceKind + \
            self.libidGuid + "#" + \
            self.version + "#" + \
            self.libidLcid + "#" + \
            self.libidPath + "#" + \
            self.libidRegName

class ReferenceRecord():
    def __init__(self, codePageName, name, libidRef):
        self.codePageName = codePageName
        encoded = name.encode(codePageName)
        self.RefName1 = SimpleRecord(0x0016, len(encoded), encoded)
        encoded = name.encode("utf_16_le")
        self.RefName2 = SimpleRecord(0x003E, len(encoded), encoded)
        self.libidRef = libidRef

    def pack(self):
        strlen = len(self.libidRef.toString())
        format = "<HII" + str(strlen) + "sIH"
        refRegistered = PackedRecord(struct.pack(format, 0x000D, strlen + 10, strlen, self.libidRef.toString().encode(self.codePageName), 0, 0))
       
        return self.RefName1.pack() + self.RefName2.pack() + refRegistered.pack()

class DoubleEncodedSimple():
    def __init__(self, codePageName, ids, text):
        self.codePageName = codePageName
        encoded = text.encode(codePageName)
        self.modName1 = SimpleRecord(ids[0], len(encoded), encoded)
        encoded = text.encode("utf_16_le")
        self.modName2 = SimpleRecord(ids[1], len(encoded), encoded)

    def pack(self):
        return self.modName1.pack() + self.modName2.pack()


class ModuleRecord():
    def __init__(self, codePageName, name, streamName, docString, offset, helpContext, cookie, type, readonly, private):
        self.codePageName = codePageName
        self.modName      = DoubleEncodedSimple(codePageName, [0x0019, 0x003E], name)
        self.streamName   = DoubleEncodedSimple(codePageName, [0x001A, 0x0032], streamName)
        self.docString    = DoubleEncodedSimple(codePageName, [0x001C, 0x0048], docString)
        self.offsetRec    = SimpleRecord(0x0031, 4, offset)
        self.helpContext  = SimpleRecord(0x001E, 4, helpContext)
        self.cookie       = SimpleRecord(0x002C, 2, helpContext)
        self.type         = PackedRecord(struct.pack("<HHI", type, 0, 0))
        #self.readonly = SimpleRecord(0x001E, 4, helpContext)
        #self.private = SimpleRecord(0x001E, 4, helpContext)
       
    def pack(self):
        output = self.codePageName.pack() + self.modName.pack() + self.streamName.pack() + self.docString.pack() + self.offsetRec.pack() + self.helpContext.pack() + self.cookie.pack() + self.type.pack()
        footer = struct.pack("<HI", 0x002B, 0)
        output += footer
        return output
