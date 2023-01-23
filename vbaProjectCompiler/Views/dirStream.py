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
        docString = DoubleEncodedString([5, 0x0040], "")
        helpfile = DoubleEncodedString([6, 0x003D], "")
        helpContext = IdSizeField(7, 4, 0)
        libFlags = IdSizeField(8, 4, 0)
        version = IdSizeField(9, 4, 0x65BE0257)
        minorVersion = PackedData("H", 17)
        constants = DoubleEncodedString([12, 0x003C], "")
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
       
    def toBytea(self):
        endien = self.project.endien
        packSymbol = '<' if endien == 'little' else '>'
        self.projectCookie = IdSizeField(19, 2, self.project.projectCookie) #should be 0xFFFF
        self.references = self.project.references
        self.modules = self.project.modules
        output = b''
        for record in self.information:
            output += record.pack(endien, codePageName)
        for record in self.references:
            output += record.pack(endien, codePageName)
        
        modulesHeader = IdSizeField(0x000F, 2, len(self.modules))

        output += modulesHeader.pack(endien, codePageName) + self.projectCookie.pack(endien, codePageName)
        for record in self.modules:
            output += record.pack(endien, codePageName)
        output += struct.pack(packSymbol + "HI", 16, 0)
        return output
