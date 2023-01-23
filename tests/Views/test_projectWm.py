import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.projectWm import ProjectWm

def test_projectWm():
    vbaProject = VbaProject()
    projectWm = ProjectWm(vbaProject)
    thisWorkbook = DocModule("ThisWorkbook")
    sheet1 = DocModule("Sheet1")
    module1 = StdModule("Module1")
    vbaProject.addModule(thisWorkbook)
    vbaProject.addModule(sheet1)
    vbaProject.addModule(module1)
    expected = b'ThisWorkbook\x00T\x00h\x00i\x00s\x00W\x00o.r.k.b.o.o.k...Sheet1.S.h.e.e.t.1...Module1.M.o.d.u.l.e.1....'

    assert projectWm.toBytes() == expected
