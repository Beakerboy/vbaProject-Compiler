from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData


class ReferenceRecord():

    def __init__(self, codepage_name, name, libidRef):
        self.codepage_name = codepage_name
        self.refname = DoubleEncodedString([0x0016, 0x003E], name)
        self.libidRef = libidRef

    def pack(self, codepage_name, endien):
        strlen = len(self.libidRef)
        format = "HII" + str(strlen) + "sIH"
        lib_str = str(self.libidRef).encode(self.codepage_name)
        refRegistered = PackedData(format, 0x000D, strlen + 10,
                                   strlen, lib_str, 0, 0)

        return (self.refname.pack(codepage_name, endien)
                + refRegistered.pack(codepage_name, endien))
