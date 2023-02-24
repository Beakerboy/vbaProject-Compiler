from vbaProjectCompiler.Models.Entities.std_module import StdModule


def test_create_cache():
    module = StdModule("Module1")
    module.cookie.value = 0xB241
    module.create_cache()

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x1200)
    file_data = f.read(0x0283)
    assert module.get_cache() == file_data


def test_set_get_cache():
    module = StdModule("Module1")
    cache = b'foo'
    module.set_cache(cache)
    assert module.get_cache() == cache
