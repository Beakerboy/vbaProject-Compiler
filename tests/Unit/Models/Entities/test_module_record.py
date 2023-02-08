import os
from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord


def test_constructor():
    module = ModuleRecord("foo")
    path1 = "vbaProjectCompiler/blank_files/ThisWorkbook.cls"
    module.add_file(path1)
    module.normalize_file()
    f = open(path1 + ".new", "r")
    path2 = "tests/blank/ThisWorkbook"
    e = open(path2, "r")
    while line := f.readline():
        assert line == e.readline()
    path3 = path1 + ".full"
    file_size = os.stat(path3)
    assert file_size.st_size == 0x03E7
    f_stream = open(path3, "rb")
    full_binary = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x0B33
    length = 0x00B3
    full_binary.seek(offset)
    container = f.read(length)
    assert f_stream.read() == container
