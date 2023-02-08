from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

def test_constructor():
    module = ModuleRecord("foo")
    path = "vbaProjectCompiler/blank_files/ThisWorkbook.cls"
    module.add_file(path)
