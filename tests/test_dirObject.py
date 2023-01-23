# test_vbaProjectCompiler.py
import pytest

from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.decompressor import Decompressor
from vbaProjectCompiler.Views.dirStream import DirStream
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord
from vbaProjectCompiler.Models.Entities.referenceRecord import ReferenceRecord


def test_dirStream():
    project = VbaProject()
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x1EC0
    f.seek(offset)
    sig = f.read(1)
    header = f.read(2)
    comp = Decompressor()
    comp.setCompressedHeader(header)
    readChunk = bytearray(f.read(comp.compressedChunkSize - 2))
    decompressedStream = comp.decompress(readChunk)
    stream = DirStream(project)
    codePage = 0x04E4
    codePageName = "cp" + str(codePage)
    libidRef = LibidReference(
        "windows",
        "{00020430-0000-0000-C000-000000000046}",
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
    libidRef2 = LibidReference(
        "windows",
        "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )
    officeReference = ReferenceRecord(codePageName, "Office", libidRef2)
    project.addReference(oleReference)
    project.addReference(officeReference)
    project.setProjectCookie(0x08F3)

    thisWorkbook = ModuleRecord("ThisWorkbook", "", 0x0333, 0, 0x0022)
    thisWorkbook.cookie.value = 0xB81C
    sheet1 = ModuleRecord("Sheet1", "", 0x0333, 0, 0x0022)
    sheet1.cookie.value = 0x9B9A
    module1 = ModuleRecord("Module1", "", 0x0283, 0, 0x0021)
    module1.cookie.value = 0xB241

    project.addModule(thisWorkbook)
    project.addModule(sheet1)
    project.addModule(module1)
    expected = bytes(decompressedStream)
    assert stream.toBytes() == expected
