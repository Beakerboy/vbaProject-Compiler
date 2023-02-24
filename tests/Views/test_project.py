import unittest.mock

from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Entities.doc_module import DocModule
from vbaProjectCompiler.Models.Entities.std_module import StdModule
from vbaProjectCompiler.Views.project import Project


class NotSoRandom():
    _rand = []

    @classmethod
    def set_seed(cls, seeds):
        cls._rand = seeds

    @classmethod
    def randint(cls, param1, param2):
        return cls._rand.pop(0)


@unittest.mock.patch('random.randint', NotSoRandom.randint)
def test_blank():
    rand = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
    NotSoRandom.set_seed(rand)
    vbaProject = VbaProject()
    vbaProject.setProjectId('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    project = Project(vbaProject)
    project.addAttribute("HelpContextID", "0")
    project.addAttribute("VersionCompatible32", "393222000")

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

    assert project.to_bytes() == expected
