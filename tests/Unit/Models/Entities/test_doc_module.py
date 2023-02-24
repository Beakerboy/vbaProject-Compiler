from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.Models.Entities.doc_module import DocModule


def test_create_cache():
    this_workbook = DocModule("ThisWorkbook")
    this_workbook.cookie.value = 0xB81C
    guid = "{00020819-0000-0000-C000-000000000046}"
    this_workbook.set_guid(guid)
    this_workbook.create_cache()

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x0800)
    file_data = f.read(0x0333)
    assert this_workbook.get_cache() == file_data


def test_create_cache2():
    module = DocModule("Sheet1")
    module.cookie.value = 0x9B9A
    guid = "{00020820-0000-0000-C000-000000000046}"
    module.set_guid(guid)
    module.create_cache()

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x0C00)
    file_data = f.read(0x0333)
    assert module.get_cache() == file_data

    
def test_normalize():
    module = DocModule("foo")
    path1 = "vbaProjectCompiler/blank_files/ThisWorkbook.cls"
    module.add_file(path1)
    guid = "{00020819-0000-0000-C000-000000000046}"
    module.set_guid(guid)
    module.normalize_file()
    f = open(path1 + ".new", "r")
    path2 = "tests/blank/ThisWorkbook"
    e = open(path2, "r")
    while line := f.readline():
        assert line == e.readline()
    path3 = path1 + ".bin"
    f_stream = open(path3, "rb")
    full_binary = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x0B33
    length = 0x00B4
    full_binary.seek(offset)
    container = full_binary.read(length)
    ms_ovba = MsOvba()
    test_data = ms_ovba.decompress(f_stream.read())
    expected_data = ms_ovba.decompress(container)
    assert test_data == expected_data
