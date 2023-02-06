from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData


class ReferenceRecord():

    def __init__(self, codePageName, name, libidRef):
        self.codePageName = codePageName
        self.RefName = DoubleEncodedString([0x0016, 0x003E], name)
        self.libidRef = libidRef

    def pack(self, codePageName, endien):
        strlen = len(self.libidRef)
        format = "HII" + str(strlen) + "sIH"
        lib_str = str(self.libidRef).encode(self.codePageName)
        refRegistered = PackedData(format, 0x000D, strlen + 10,
                                   strlen, lib_str, 0, 0)

        return (self.RefName.pack(codePageName, endien)
                + refRegistered.pack(codePageName, endien))
