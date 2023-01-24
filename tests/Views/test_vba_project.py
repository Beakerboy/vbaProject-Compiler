import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.vba_Project import Vba_Project

def test_projectWm():
    vbaProject = VbaProject()
    vba_Project = Vba_Project(vbaProject)
    expected = b'\xCC\x61\xFF\xFF\x00\x03\x00'
    result = vba_Project.toBytes()
    assert vba_Project.toBytes() == expected
    vbaProject.setPerformanceCache(b'\x00\x01\x02\x03')
    vbaProject.setPerformanceCacheVersion(0x00B5)
    expected = b'\xCC\x61\xB5\x00\x00\x03\x00\x00\x01\x02\x03'
    assert vba_Project.toBytes() == expected

def test_realData():
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x14C0
    f.seek(offset)
    data = f.read(0x0410).decode("utf_16_le")
    assert data == "nope"
    
