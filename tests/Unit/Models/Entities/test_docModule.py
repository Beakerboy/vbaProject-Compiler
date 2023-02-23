from vbaProjectCompiler.Models.Entities.docModule import DocModule


test_create_cache():
    this_workbook = DocModule("ThisWorkbook")
    this_workbook.cookie.value = 0xB81C
    guid = "{00020819-0000-0000-C000-000000000046}"
    thisWorkbook.addVbBase(guid)
    thisWorkbook.create_cache()

    f = open('tests/blank/vbaProject.bin', 'rb')
    f.seek(0x080)
    file_data = f.read(0x0333)
    assert this_workbook.get_cache() == file_data
