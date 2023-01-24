import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.vba_Project import Vba_Project

def test_projectWm():
    vbaProject = VbaProject()
    vba_Project = Vba_Project(vbaProject)
    vbaProject.setPerformanceCacheVersion(0x61CC)
    expected = b'\xCC\x61\xB5\x00\x00\x03\x00'
    result = vba_Project.toBytes()
    assert vba_Project.toBytes() == expected
    vbaProject.setPerformanceCache(b'\x00\x01\x02\x03')
    expected = b'\xCC\x61\xB5\x00\x00\x03\x00\x00\x01\x02\x03'
    assert vba_Project.toBytes() == expected
