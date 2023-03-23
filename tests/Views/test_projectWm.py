from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Entities.doc_module import DocModule
from vbaProjectCompiler.Models.Entities.std_module import StdModule
from vbaProjectCompiler.Views.projectWm import ProjectWm


def test_project_wm() -> None:
    vba_project = VbaProject()
    project_wm = ProjectWm(vba_project)
    this_workbook = DocModule("ThisWorkbook")
    sheet1 = DocModule("Sheet1")
    module1 = StdModule("Module1")
    vba_project.addModule(this_workbook)
    vba_project.addModule(sheet1)
    vba_project.addModule(module1)
    expected = (b'ThisWorkbook\x00T\x00h\x00i\x00s\x00W\x00o\x00r\x00k\x00b'
                + b'\x00o\x00o\x00k\x00\x00\x00Sheet1\x00S\x00h\x00e\x00e\x00'
                + b't\x001\x00\x00\x00Module1\x00M\x00o\x00d\x00u\x00l\x00e'
                + b'\x001\x00\x00\x00\x00\x00')
    result = project_wm.to_bytes()
    assert len(result) == 86
    assert result == expected
