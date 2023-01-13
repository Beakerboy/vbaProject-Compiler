# test_project.py

import pytest
from vbaProjectCompiler.project import Project
from pathlib import Path

def test_blank():
    project = Project()
    project.addAttribute("HelpContextID", "0")
    project.addAttribute("VersionCompatible32", "393222000")
    project.addAttribute("CMG", "41435A5A5E5A5E5A5E5A5E")
    project.addAttribute("DPB", "BCBEA7A2591C5A1C5A1C")
    project.addAttribute("GC", "37352C2BDCDD56DE56DEA9")

    project.hostExtenderInfo = "&H00000001={3832D640-CF90-11CF-8E43-00A0C911005A};VBE;&H00000000"

    project.addWorkspace("ThisWorkbook", 0, 0, 0, 0, 'C')
    project.addWorkspace("Sheet1", 0, 0, 0, 0, 'C')
    project.addWorkspace("Module1", 26, 26, 1349, 522, 'Z')
    
    #expected = Path("tests/blank/vbaProject.bin").read_text()
    file = open("tests/blank/vbaProject.bin", "rb")
    file.seek(int('0x2400', 0))
    expected = file.read(int('0x152', 0))

    result = project.toBytearray()
    assert expected == result
