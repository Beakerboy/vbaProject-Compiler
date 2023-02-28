import os
import uuid
from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.Models.Entities.doc_module import DocModule


def test_normalize():
    module = DocModule("foo")
    path1 = "vbaProjectCompiler/blank_files/ThisWorkbook.cls"
    os.remove(path1 + ".new")
    module.add_file(path1)
    module.cookie.value = 0xB81C
    guid = uuid.UUID('0002081900000000C000000000000046')
    module.set_guid(guid)
    module.normalize_file()
    f = open(path1 + ".new", "rb")
    path2 = "tests/blank/ThisWorkbook"
    e = open(path2, "rb")
    assert f.read() == e.read()
    # while line := f.readline():
    #     assert line == e.readline()

    module.create_cache()
    module.write_file()
    path3 = path1 + ".bin"
    f_stream = open(path3, "rb")
    full_binary = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x0800
    length1 = 0x0333
    length2 = 0x00B4
    full_binary.seek(offset)
    cache = full_binary.read(length1)
    assert f_stream.read(0x333) == cache

    container = full_binary.read(length2)
    ms_ovba = MsOvba()
    test_data = ms_ovba.decompress(f_stream.read())
    expected_data = ms_ovba.decompress(container)
    assert test_data == expected_data
