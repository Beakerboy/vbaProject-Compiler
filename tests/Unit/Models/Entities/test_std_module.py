from vbaProjectCompiler.Models.Entities.stdModule import StdModule


def test_create_cache():
    module = StdModule("Module1")
    module.cookie.value = 0xB241
    module.create_cache()

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x1200)
    file_data = f.read(0x0283)
    assert module.get_cache() == file_data
