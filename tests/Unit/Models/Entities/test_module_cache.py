import uuid
from vbaProjectCompiler.Models.Entities.module_cache import ModuleCache


def test_module_cache():
    cache = ModuleCache()
    cache.cookie = 0xB81C
    cache.misc = [0x0316, 0x02D2, 0x032D, 0x0123, 0x88, 8, 0x18, "00000000", 0]
    guid = uuid.UUID('0002081900000000C000000000000046')
    cache.guid = bytes(("0{" + str(guid) + "}").upper(), "utf_16_le")
    cache.guids1 = b'\xff' * 4 + b'\x00' * 54
    
    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                    "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                    "02 3C FF FF FF FF 00 00")
    cache.object_table = bytes.fromhex(" ".join(object_table))
    cache.pcode = b''

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x0800)
    file_data = f.read(0x0333)
    assert cache.to_bytes() == file_data
