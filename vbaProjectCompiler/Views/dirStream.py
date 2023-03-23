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

    def __init__(self, project) -> None:
        self.project = project
        self.codepage = 0x04E4
        # 0=16bit, 1=32bit, 2=mac, 3=64bit
        syskind = IdSizeField(1, 4, 3)
        compat_version = IdSizeField(74, 4, 3)
        lcid = IdSizeField(2, 4, 0x0409)
        lcid_invoke = IdSizeField(20, 4, 0x0409)
        codepage_record = IdSizeField(3, 2, self.codepage)
        project_name = IdSizeField(4, 10, "VBAProject")
        docstring = DoubleEncodedString([5, 0x0040], "")
        helpfile = DoubleEncodedString([6, 0x003D], "")
        help_context = IdSizeField(7, 4, 0)
        lib_flags = IdSizeField(8, 4, 0)
        version = IdSizeField(9, 4, 0x65BE0257)
        minor_version = PackedData("H", 17)
        constants = DoubleEncodedString([12, 0x003C], "")
        self.information = [
            syskind,
            compat_version,
            lcid,
            lcid_invoke,
            codepage_record,
            project_name,
            docstring,
            helpfile,
            help_context,
            lib_flags,
            version,
            minor_version,
            constants
        ]
        self.references = []
        self.modules = []

    def to_bytes(self) -> bytes:
        endien = self.project.endien
        codepage_name = self.project.getCodePageName()
        pack_symbol = '<' if endien == 'little' else '>'
        # should be 0xFFFF
        cookie_value = self.project.projectCookie
        self.project_cookie = IdSizeField(19, 2, cookie_value)
        self.references = self.project.references
        self.modules = self.project.modules
        output = b''
        for record in self.information:
            output += record.pack(codepage_name, endien)
        for record in self.references:
            output += record.pack(codepage_name, endien)

        modules_header = IdSizeField(0x000F, 2, len(self.modules))

        output += (modules_header.pack(codepage_name, endien)
                   + self.project_cookie.pack(codepage_name, endien))
        for record in self.modules:
            output += record.pack(codepage_name, endien)
        output += struct.pack(pack_symbol + "HI", 16, 0)
        return output

    def write_file(self):
        bin_f = open("dir.bin", "wb")
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(self.to_bytes())
        bin_f.write(compressed)
        bin_f.close()
