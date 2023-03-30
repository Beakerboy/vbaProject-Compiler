from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData


class ReferenceRecord():

    def __init__(self, codepage_name, name, libid_ref):
        # is self._codepage_name even needed?
        self._codepage_name = codepage_name
        self._refname = DoubleEncodedString([0x0016, 0x003E], name)
        self._libid_ref = libid_ref

    def pack(self, codepage_name, endien):
        strlen = len(self._libid_ref)
        format = "HII" + str(strlen) + "sIH"
        lib_str = str(self._libid_ref).encode(self._codepage_name)
        ref_registered = PackedData(format, 0x000D, strlen + 10,
                                   strlen, lib_str, 0, 0)

        return (self._refname.pack(codepage_name, endien)
                + ref_registered.pack(codepage_name, endien))
