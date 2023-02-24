from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField


class ModuleBase():
    def __init__(self, name):
        """
        Initialize the module record
        """
        self.modName = DoubleEncodedString([0x0019, 0x0047], name)
        self.streamName = DoubleEncodedString([0x001A, 0x0032], name)
        self.docString = DoubleEncodedString([0x001C, 0x0048], "")
        self.helpContext = IdSizeField(0x001E, 4, 0)
        self.cookie = IdSizeField(0x002C, 2, 0xFFFF)

        # self.readonly = SimpleRecord(0x001E, 4, helpContext)
        # self.private = SimpleRecord(0x001E, 4, helpContext)
        self._cache = b''
        self.workspace = [0, 0, 0, 0, 'C']
        self.type = ''
        self.created = 0
        self.modified = 0
        self._fileSize = 0
        self._size = 0

    def set_cache(self, cache):
        self._cache = cache

    def get_cache(self):
        return self._cache

    def addWorkspace(self, val1, val2, val3, val4, val5):
        self.workspace = [val1, val2, val3, val4, val5]

    def pack(self, codePageName, endien):
        """
        Pack the metadata for use in the dir stream.
        """
        typeIdValue = 0x0022 if self.type == 'Document' else 0x0021
        typeId = PackedData("HI", typeIdValue, 0)
        self.offsetRec = IdSizeField(0x0031, 4, len(self._cache))
        output = (self.modName.pack(codePageName, endien)
                  + self.streamName.pack(codePageName, endien)
                  + self.docString.pack(codePageName, endien)
                  + self.offsetRec.pack(codePageName, endien)
                  + self.helpContext.pack(codePageName, endien)
                  + self.cookie.pack(codePageName, endien)
                  + typeId.pack(codePageName, endien))
        footer = PackedData("HI", 0x002B, 0)
        output += footer.pack(codePageName, endien)
        return output

    def toProjectModuleString(self):
        return self.type + "=" + self.modName.value

    def add_file(self, file_path):
        self._file_path = file_path

    def getData(self):
        """
        """
        # Read the compresses file
        # Combine it with the performanceCache
        return self._cache

    def _attr(self, name, value):
        return 'Attribute VB_' + name + ' = ' + value + '\n'

    def _create_cache_header(self, cookie, c1, id_table,
                             c4, c5, c8, c6, c7) -> bytes:
        """
        Create the header for the performance cache
        id_table is the start of the indirect table.
        magic_ofs is 3C less than the offset of the magic code.
        """
        co = cookie.value.to_bytes(2, "little").hex()
        obj_table_ofs = (0x017A - 0x8A).to_bytes(4, "little").hex()
        ca = ("01 16 03 00 00", obj_table_ofs, c1.hex(), "02 00 00 D4 00 00",
              "00", id_table.hex(), "00 00 FF FF FF FF 00 00 00 00",
              c4.hex(), "00",
              "00 00 00 00 00 01 00 00 00 F3 08", co, "00 00 FF",
              "FF", c5.hex(), "00 00", c8.hex(),
              "00 00 00 B6 00 FF FF 01 01 00",
              "00 00 00 FF FF FF FF 00 00 00 00 FF FF FF FF FF",
              "FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
              "00 " * (16 * 2 - 1) + " 00",
              "00 00 00 00 00 00 00 10 00 00 00 03 00 00 00 05",
              "00 00 00 07 00 00 00 FF FF FF FF FF FF FF FF 01",
              "01 08 00 00 00 FF FF FF FF 78 00 00 00", c6.hex(), "00 00",
              "00 " * 15 + " 00",
              "00 " * 14 + " FF FF",
              "00 00 00 00 4D 45 00 00 FF FF FF FF FF FF 00 00",
              "00 00 FF FF 00 00 00 00 FF FF 01 01 00 00 00 00",
              "DF 00 FF FF 00 00 00 00", c7.hex(), "FF FF FF FF FF FF",
              "FF " * (16 * 7 + 9) + " FF")
        return bytes.fromhex(" ".join(ca))

    def _create_cache_footer(self, c1) -> bytes:
        fo = ("00 00 00 00 00 00 00 00"
              "FF FF FF FF FF FF FF FF FF FF FF FF", c1.hex() * 4,
              "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
              "FF FF FF FF", c1.hex() * 4, "FF FF FF FF FF FF FF FF",
              "FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00",
              "00 00 00 00 FF FF 00 00 FF FF FF FF FF FF 00 00",
              "00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF",
              "FF FF FF FF FF FF FF FF FF FF 00 00 FF FF FF FF",
              "FF FF 00 00 00 00 00 00 DF 00 00 00 00 00 00 00",
              "00 " * 16 * 3,
              "00 00 00 00 00")
        return bytes.fromhex(" ".join(fo))

    def _create_pcode(self) -> bytes:
        pcode = ("FE CA 01 00 00 00 FF FF FF FF 01",
                 "01 08 00 00 00 FF FF FF FF 78 00 00 00 FF FF FF",
                 "FF 00 00")
        return bytes.fromhex(" ".join(pcode))

    def _create_cache_middle(self, object_table, data2,
                             indirect_table) -> bytes:
        data2_bytes = b''
        for msg in data2:
            data2_bytes += msg
        size1 = len(object_table).to_bytes(4, "little")
        size2 = len(data2).to_bytes(2, "little")
        size3 = len(indirect_table).to_bytes(4, "little")
        ca = (size1 + object_table
              + b'\xFF\xFF\x01\x01\x00\x00\x00\x00'
              + size2 + data2_bytes
              + b'\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01'
              + size3 + indirect_table
              + b'\x00\x00\xFF\xFF\x00\x00')
        return ca