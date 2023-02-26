from vbaProjectCompiler.Models.Entities.module_cache import ModuleCache


def test_module_cache():
    cache = ModuleCache()
    cache.cookie = 0xB81C
    cache.misc = [0x0316, 0x02D2, 0x032D, 0x0123, 0x88, 0, 0, 0, 0]
    cache.guids1 = b'\xff' * 4 + b'\x00' * 54
    
    cache.indirect_table = 0x0200.to_bytes(2, "little")
    
    cache.object_table = b''
    cache.pcode = b''

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x0800)
    file_data = f.read(0x0333)
    assert cache.to_bytes() == file_data
