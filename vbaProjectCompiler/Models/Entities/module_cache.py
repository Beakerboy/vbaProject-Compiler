import struct


class ModuleCache():

    def __init__(self):
        self.cookie = 0
        self.misc = []
        self.guids1 = b'\xff' * 4 + b'\x00' * 54
        self.guids2 = guids2 = b'\x00' * 32
        self.indirect_table = b''
        self.object_table = b''
        self.pcode = b''

    def to_bytes(self) -> bytes:
        oto = self.object_table_offset() - 0x8A
        ito = self.id_table_offset() - 10
        magic_ofs = self.magic_offset() - 0x3C
        ca = struct.pack("<BIIHHIHHiIHIHIHHHhHHHHHhHIiIh", 1, self.misc[0],
                         oto, self.misc[1], 0, 0xD4, ito, 0, -1, magic_ofs,
                         self.misc[2], 0, 0, 1, 0x08F3, self.cookie,
                         0, -1, self.misc[3], 0, self.misc[4], 0,
                         0xB6, -1, 0x0101, 0, -1, 0, -1)
        ca += self.guids1
        ca += struct.pack("<IIIIiiHIiIB", 0x10, 3, 5, 7, -1, -1, 0x0101,
                          8, -1, 0x78, self.misc[5])
        ca += self.guids2
        ca += struct.pack("<hIIihIhIhHIHhIH", -1, 0, 0x454D, -1, -1, 0, -1,
                          0, -1, 0x0101, 0, 0xDF, -1, 0, self.misc[6])
        ca += b'FF' * 0x80
        return ca

    def object_table_offset(self) -> int:
        """
        The object table offset is 8A less than the position.
        The object table is between the block of F's and the
        Utf-16 Guid.
        """
        return 0x0140 + len(self.guids1)

    def id_table_offset(self) -> int:
        return 0x020A

    def magic_offset(self):
        return self.id_table_offset() + 0x10B
        
    def set_id_table(self, table):
        self.indirect_table = table

    def pcode_offset(self) -> int:
        """
        The pcode section begins with the magic code 0xCAFE
        """
        pass

    def _create_cache_header(self, cookie, c1, id_table,
                             c4, c5, c8, c6, c7) -> bytes:
        """
        Create the header for the performance cache
        id_table is the start of the indirect table.
        magic_ofs is 3C less than the offset of the magic code.
        """
        co = cookie.value.to_bytes(2, "little").hex()
        obj_table_ofs = (0x017A - 0x8A).to_bytes(4, "little").hex()
        guids = "FF FF FF FF " + "00 " * 54
        guids2 = "00 " * 32
        ca = ("01 16 03 00 00", obj_table_ofs, c1.hex(), "02 00 00 D4 00 00",
              "00", id_table.hex(), "00 00 FF FF FF FF 00 00 00 00",
              c4.hex(), "00",
              "00 00 00 00 00 01 00 00 00 F3 08", co, "00 00 FF",
              "FF", c5.hex(), "00 00", c8.hex(),
              "00 00 B6 00 FF FF 01 01 00",
              "00 00 00 FF FF FF FF 00 00 00 00 FF FF",
              guids,
              "10 00 00 00 03 00 00 00 05 00 00 00 07 00 00 00",
              "FF FF FF FF FF FF FF FF 01 01 08 00 00 00 FF FF",
              "FF FF 78 00 00 00", c6.hex(), guids2,
              "FF FF",
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
