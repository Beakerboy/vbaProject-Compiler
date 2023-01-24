import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
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
    data = f.read(0x0470)
    libs = []
    delim = []
    libs.append(LibidReference(
        "windows",
        "{000204EF-0000-0000-C000-000000000046}",
        "4.2",
        9,
        "C:\Program Files\Common Files\Microsoft Shared\VBA\VBA7.1\VBE7.DLL",
        "Visual Basic For Applications"
    ))
    delim.append(0x011A)
    libs.append(LibidReference(
        "windows",
        "{00020813-0000-0000-C000-000000000046}",
        "1.9",
        0,
        "C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "Microsoft Excel 16.0 Object Library"
    ))
    delim.append(0x00BC)
    libs.append(LibidReference(
        "windows",
        "{00020430-0000-0000-C000-000000000046}",
        "2.0",
        0,
        "C:\Windows\System32\stdole2.tlb",
        "OLE Automation"
    ))
    delim.append(0x0128)
    libs.append(LibidReference(
        "windows",
        "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
        "2.8",
        0,
        "C:\Program Files\Common Files\Microsoft Shared\OFFICE16\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    ))
    expected = b''
    i = 0
    for lib in libs:
        expected += bytearray(str(libs), "utf_16_le") + struct.pack("<HHHH", 0, 0, 0, delim[i])
        i += 1
    assert expected == data
