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

def test_realData():
    vbaProject = VbaProject()
    vba_Project = Vba_Project(vbaProject)
    vbaProject.setPerformanceCacheVersion(0x00B5)
    thisWorkbook = DocModule("ThisWorkbook")
    thisWorkbook.cookie.value = 0xB81C
    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x14C0
    f.seek(offset)
    data = f.read(0x0700)
    libraries = []
    delim = []
    libraries.append(LibidReference(
        "windows",
        "{000204EF-0000-0000-C000-000000000046}",
        "4.2",
        "9",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\VBA\\VBA7.1\\VBE7.DLL",
        "Visual Basic For Applications"
    ))
    delim.append(0x011A)
    libraries.append(LibidReference(
        "windows",
        "{00020813-0000-0000-C000-000000000046}",
        "1.9",
        "0",
        "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Microsoft Excel 16.0 Object Library"
    ))
    delim.append(0x00BC)
    libraries.append(LibidReference(
        "windows",
        "{00020430-0000-0000-C000-000000000046}",
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    ))
    delim.append(0x0128)
    libraries.append(LibidReference(
        "windows",
        "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
        "2.8",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    ))
    delim.append(0x0003)
    cache = b'\xFF\x09\x04\x00\x00\x09\x04\x00\x00\xE4\x04\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x04\x00\x02\x00\x20\x01'
    i = 0
    for lib in libraries:
        cache += bytearray(str(lib), "utf_16_le") + struct.pack("<IIIH", 0, 0, 0, delim[i])
        i += 1
    cache += struct.pack("<17H", 2, 2, 1, 6, 0x0212, 0, 0x0214, 1, 0x0216, 1, 0x0218, 0 , 0x021a, 1 , 0x021c, 1, 0x0222) + bytearray('\xFF' * 36, 'charmap')
    prefix = [0x0018, 0x000C, 0x000E]
    index = 0x0046
    i = 0
    for module in vbaProject.modules:
        name = module.modName.value.encode("utf_16_le")
        cache += struct.pack("<H", prefix[i]) + name + struct.pack("<HH", 0x0014, 0x0032) + chr(69 + i) + "65be0257".encode("utf_16_le") + struct.pack("<HHH", 0xFFFF, 0x0227, prefix[i]) + name + struct.pack("<HHHI", 0xFFFF, module.cookie.value, 0, 0)
        i += 1
    vbaProject.setPerformanceCache(cache)
    assert vba_Project.toBytes() == data
