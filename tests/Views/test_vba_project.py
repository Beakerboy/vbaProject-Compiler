import pytest
import struct
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
from vbaProjectCompiler.Models.Entities.docModule import DocModule
from vbaProjectCompiler.Models.Entities.stdModule import StdModule
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
