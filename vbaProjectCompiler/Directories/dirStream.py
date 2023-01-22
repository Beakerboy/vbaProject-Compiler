import struct
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField
from vbaProjectCompiler.Models.Fields.doubleEncodedString import DoubleEncodedString
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class DirStream(StreamDirectory):
    """
    The dir stream is compressed on write
    """

    def __init__(self):
        self.codePage = 0x04E4
        codePageName = "cp" + str(self.codePage)
        syskind = IdSizeField(1, 4, 3) #0=16bit, 1=32bit, 2=mac, 3=64bit
        compatVersion = IdSizeField(74, 4, 3)
        lcid = IdSizeField(2, 4, 0x0409)
        lcidInvoke = IdSizeField(20, 4, 0x0409)
        codePageRecord = IdSizeField(3, 2, self.codePage)
        projectName = IdSizeField(4, 10, "VBAProject")
        docString = DoubleEncodedString(codePageName, [5, 0x0040], "")
        helpfile = DoubleEncodedString(codePageName, [6, 0x003D], "")
        helpContext = IdSizeField(7, 4, 0)
        libFlags = IdSizeField(8, 4, 0)
        version = IdSizeField(9, 4, 0x65BE0257)
        minorVersion = PackedData("H", 17)
        constants = DoubleEncodedString(codePageName, [12, 0x003C], "")
        self.information = [
            syskind,
            compatVersion,
            lcid,
            lcidInvoke,
            codePageRecord,
            projectName,
            docString,
            helpfile,
            helpContext,
            libFlags,
            version,
            minorVersion,
            constants
        ]
        self.references  = []
        
        thisWorkbook = ModuleRecord(codePageName, "ThisWorkbook", "ThisWorkbook", "", 0x0333, 0, 0xB81C, 0x0022)
        sheet1 = ModuleRecord(codePageName, "Sheet1", "Sheet1", "", 0x0333, 0, 0x9B9A, 0x0022)
        module1 = ModuleRecord(codePageName, "Module1", "Module1", "", 0x0283, 0, 0xB241, 0x0021)
        self.modules = [thisWorkbook, sheet1, module1]

    def addReference(self, ref):
        self.references.append(ref)

    def toBytes(self):
        output = b''
        for record in self.information:
            output += record.pack()
        for record in self.references:
            output += record.pack()
        
        modulesHeader = IdSizeField(0x000F, 2, len(self.modules))
        cookie = IdSizeField(19, 2, 0x08F3) #should be 0xFFFF
        output += modulesHeader.pack() + cookie.pack()
        for record in self.modules:
            output += record.pack()
        output += struct.pack("<HI", 16, 0)
        return output
