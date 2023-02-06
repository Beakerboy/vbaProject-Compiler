from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Entities.docModule import DocModule
from vbaProjectCompiler.Models.Entities.stdModule import StdModule
from vbaProjectCompiler.Views.project import Project


def test_blank():
    vbaProject = VbaProject()
    vbaProject.setProjectId('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    project = Project(vbaProject)
    project.addAttribute("HelpContextID", "0")
    project.addAttribute("VersionCompatible32", "393222000")
    vbaProject.setProtectionState("41435A5A5E5A5E5A5E5A5E")
    vbaProject.setPassword("BCBEA7A2591C5A1C5A1C")
    vbaProject.setVisibilityState("37352C2BDCDD56DE56DEA9")

    project.hostExtenderInfo = ("&H00000001="
                                + "{3832D640-CF90-11CF-8E43-00A0C911005A};VBE;"
                                + "&H00000000")

    thisWorkbook = DocModule("ThisWorkbook")
    sheet1 = DocModule("Sheet1")
    module1 = StdModule("Module1")
    module1.addWorkspace(26, 26, 1349, 522, 'Z')

    vbaProject.addModule(thisWorkbook)
    vbaProject.addModule(sheet1)
    vbaProject.addModule(module1)

    # expected = Path("tests/blank/vbaProject.bin").read_text()
    file = open("tests/blank/vbaProject.bin", "rb")
    file.seek(0x2180)
    expected = file.read(0x0080)
    file.seek(0x2400)
    expected += file.read(0x0152)

    assert project.toBytearray() == expected
