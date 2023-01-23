# test_project.py

import pytest
from pathlib import Path
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord
from vbaProjectCompiler.Views.project import Project

def test_blank():
    vbaProject = VbaProject()
    project = Project(vbaProject)
    project.addAttribute("HelpContextID", "0")
    project.addAttribute("VersionCompatible32", "393222000")
    project.addAttribute("CMG", "41435A5A5E5A5E5A5E5A5E")
    project.addAttribute("DPB", "BCBEA7A2591C5A1C5A1C")
    project.addAttribute("GC", "37352C2BDCDD56DE56DEA9")

    project.hostExtenderInfo = "&H00000001={3832D640-CF90-11CF-8E43-00A0C911005A};VBE;&H00000000"

    thisWorkbook = ModuleRecord("ThisWorkbook", 0x0022)
    sheet1 = ModuleRecord("Sheet1", 0x0022)
    module1 = ModuleRecord("Module1", 0x0021)
    module1.addWorkspace(26, 26, 1349, 522, 'Z')

    vbaProject.addModule(thisWorkbook)
    vbaProject.addModule(sheet1)
    vbaProject.addModule(module1)

    #expected = Path("tests/blank/vbaProject.bin").read_text()
    file = open("tests/blank/vbaProject.bin", "rb")
    file.seek(0x2180)
    expected = file.read(0x0080)
    file.seek(0x0200)
    expected += file.read(0x0152)

    result = project.toBytearray()
    assert expected == result
