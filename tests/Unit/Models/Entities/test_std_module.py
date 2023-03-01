from vbaProjectCompiler.Models.Entities.std_module import StdModule


def test_set_get_cache():
    module = StdModule("Module1")
    cache = b'foo'
    module.set_cache(cache)
    assert module.get_cache() == cache


def test_get_name():
    module = StdModule("Module1")
    assert module.get_name() == "Module1"
