from vbaProjectCompiler.Models.Entities.module_cache import ModuleCache


test_module_cache():
    cache = ModuleCache()
    cache.cookie
    cache.misc = []
    cache.guids1 = b'\xff' * 4 + b'\x00' * 54
    cache.indirect_table = b''
    cache.object_table = b''
    cache.pcode = b''
    assert cache.to_bytes() == b''
