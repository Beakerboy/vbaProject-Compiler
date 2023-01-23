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

    def __init__(self, project):
        self.project = project
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
        self.modules = []
        self.projectCookie = IdSizeField(19, 2, 0xFFFF) #should be 0xFFFF

    def toBytes(self):
        self.references = self.project.references
        self.modules = self.project.modules
        output = b''
        for record in self.information:
            output += record.pack()
        for record in self.references:
            output += record.pack()
        
        modulesHeader = IdSizeField(0x000F, 2, len(self.modules))

        output += modulesHeader.pack() + self.projectCookie.pack()
        for record in self.modules:
            output += record.pack()
        output += struct.pack("<HI", 16, 0)
        return output
