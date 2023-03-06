import struct
from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField
from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData


class DirStream():
    """
    The dir stream is compressed on write
    """

    def __init__(self, project):
        self.project = project
        self.codePage = 0x04E4
        # 0=16bit, 1=32bit, 2=mac, 3=64bit
        syskind = IdSizeField(1, 4, 3)
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
        self.references = []
        self.modules = []

    def to_bytes(self):
        endien = self.project.endien
        codePageName = self.project.getCodePageName()
        packSymbol = '<' if endien == 'little' else '>'
        # should be 0xFFFF
        cookie_value = self.project.projectCookie
        self.projectCookie = IdSizeField(19, 2, cookie_value)
        self.references = self.project.references
        self.modules = self.project.modules
        output = b''
        for record in self.information:
            output += record.pack(codePageName, endien)
        for record in self.references:
            output += record.pack(codePageName, endien)

        modulesHeader = IdSizeField(0x000F, 2, len(self.modules))

        output += (modulesHeader.pack(codePageName, endien)
                   + self.projectCookie.pack(codePageName, endien))
        for record in self.modules:
            output += record.pack(codePageName, endien)
        output += struct.pack(packSymbol + "HI", 16, 0)
        return output

    def write_file(self):
        bin_f = open("dir.bin", "wb")
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(self.to_bytes())
        bin_f.write(compressed)
        bin_f.close()
