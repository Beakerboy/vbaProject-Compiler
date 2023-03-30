from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData


class ReferenceRecord():

    def __init__(self, codepage_name, name, libid_ref):
        # is this even needed?
        self._codepage_name = codepage_name
        self._refname = DoubleEncodedString([0x0016, 0x003E], name)
        self._libid_ref = libid_ref

    def pack(self, codepage_name, endien):
        strlen = len(self.libidRef)
        format = "HII" + str(strlen) + "sIH"
        lib_str = str(self._libid_ref).encode(self._codepage_name)
        refRegistered = PackedData(format, 0x000D, strlen + 10,
                                   strlen, lib_str, 0, 0)

        return (self._refname.pack(codepage_name, endien)
                + refRegistered.pack(codepage_name, endien))
