from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord


class DocModule(ModuleRecord):
    """
    A Document Module is a module record that is associated with a worksheet or
    workbook.
    """
    def __init__(self, name):
        self.docTlibVer = 0
        super(DocModule, self).__init__(name)
        self.type = "Document"

        # GUID
        self._vbBase = ""

    def toProjectModuleString(self):
        return ("Document=" + self.modName.value + "/&H"
                + self.docTlibVer.to_bytes(4, "big").hex())

    def addVbBase(self, guid):
        """
        Should probably abstract this to add other attributes to the file
        during normalization.
        """
        self._vbBase = guid

    def create_cache(self):
        guid = '0' + self._vbBase
        guid_bytes = bytes(guid, "utf_16_le")
        guid_size = len(guid_bytes).to_bytes(2, "little")
        data = ("00 00 02 00",
                "53 4C FF FF FF FF 00 00 01 00 53 10 FF FF FF FF",
                "00 00 01 00 53 94 FF FF FF FF 00 00 00 00 02 3C",
                "FF FF FF FF")
        ca = self._create_cache_header(self.cookie, b'\xD2', b'\x00\x02',
                                       b'\xD9', b'\x2D\x03', b'\x23\x01',
                                       b'\x08', b'\x18')
        data1 = (guid_size + guid_bytes)
        d2 = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF"
              "30\x00\x00\x00\x02\x01\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00'
              "FF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x2E\x00\x43\x00'
              "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
        ca = (ca + self._create_cache_middle(ms, data1, d2)
          + b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + self._create_cache_footer(b'\00'))
        return ca
