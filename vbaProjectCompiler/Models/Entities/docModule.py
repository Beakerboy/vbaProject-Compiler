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
        ms = (b'\x00\x00\x02\x00'
          + b'\x53\x4C\xFF\xFF\xFF\xFF\x00\x00\x01\x00\x53\x10\xFF\xFF\xFF\xFF'
          + b'\x00\x00\x01\x00\x53\x94\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x02\x3C'
          + b'\xFF\xFF\xFF\xFF')
        ca = self._create_cache_header(self.cookie, b'\xD2', b'\x00\x02', b'\xD9',
                               b'\x2D\x03', b'\x23\x01', b'\x08', b'\x18')
        data1 = (guid_size + guid_bytes)
        d2 = (b''
          + b'\x02\x80\xFE\xFF\xFF\xFF\xFF\xFF\x20\x00\x00\x00\xFF\xFF\xFF\xFF'
          + b'\x30\x00\x00\x00\x02\x01\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x2E\x00\x43\x00'
          + b'\x1D\x00\x00\x00\x25\x00\x00\x00\xFF\xFF\xFF\xFF\x40\x00\x00\x00'
          + b'')
        ca = (ca + self._create_cache_middle(ms, data1, d2)
          + b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + self._create_cache_footer(b'\00'))
        return ca
