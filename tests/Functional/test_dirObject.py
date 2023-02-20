from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.dirStream import DirStream
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
from vbaProjectCompiler.Models.Entities.docModule import DocModule
from vbaProjectCompiler.Models.Entities.stdModule import StdModule
from vbaProjectCompiler.Models.Entities.referenceRecord import ReferenceRecord


def test_dirStream():

    # Read the data from the demo file and decompress it.
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x1EC0
    length = 0x0232
    f.seek(offset)
    container = f.read(length)
    ms_ovba = MsOvba()
    decompressedStream = ms_ovba.decompress(container)

    # Create a project with the same attributes
    project = VbaProject()
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

    thisWorkbook = DocModule("ThisWorkbook")
    thisWorkbook.cookie.value = 0xB81C
    ca = (b'\x01\x16\x03\x00\x00\xF0\x00\x00\x00\xD2\x02\x00\x00\xD4\x00\x00'
          + b'\x00\x00\x02\x00\x00\xFF\xFF\xFF\xFF\xD9\x02\x00\x00\x2D\x03\x00'
          + b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\xF3\x08\x1C\xB8\x00\x00\xFF'
          + b'\xFF\x23\x01\x00\x00\x88\x00\x00\x00\xB6\x00\xFF\xFF\x01\x01\x00'
          + b'\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x03\x00\x00\x00\x05'
          + b'\x00\x00\x00\x07\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01'
          + b'\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\x08\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF'
          + b'\x00\x00\x00\x00\x4D\x45\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00'
          + b'\x00\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00'
          + b'\xDF\x00\xFF\xFF\x00\x00\x00\x00\x18\x00\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x28\x00\x00\x00\x02\x00'
          + b'\x53\x4C\xFF\xFF\xFF\xFF\x00\x00\x01\x00\x53\x10\xFF\xFF\xFF\xFF'
          + b'\x00\x00\x01\x00\x53\x94\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x02\x3C'
          + b'\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\x01\x00'
          + b'\x4E\x00\x30\x00\x7B\x00\x30\x00\x30\x00\x30\x00\x32\x00\x30\x00'
          + b'\x38\x00\x31\x00\x39\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00'
          + b'\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x2D\x00\x43\x00\x30\x00'
          + b'\x30\x00\x30\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00'
          + b'\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x34\x00\x36\x00\x7D\x00'
          + b'\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01\x40\x00\x00\x00'
          + b'\x02\x80\xFE\xFF\xFF\xFF\xFF\xFF\x20\x00\x00\x00\xFF\xFF\xFF\xFF'
          + b'\x30\x00\x00\x00\x02\x01\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x2E\x00\x43\x00'
          + b'\x1D\x00\x00\x00\x25\x00\x00\x00\xFF\xFF\xFF\xFF\x40\x00\x00\x00'
          + b'\x00\x00\xFF\xFF\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00'
          + b'\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\x00\x00\x00\x00\x00\x00\xDF\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\xFE\xCA\x01\x00\x00\x00\xFF\xFF\xFF\xFF\x01'
          + b'\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\xFF\xFF\xFF'
          + b'\xFF\x00\x00')
    thisWorkbook.addPerformanceCache(ca)

    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    sheet1.addPerformanceCache(ca)

    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    ca = (b'\x01\x16\x03\x00\x00\xF0\x00\x00\x00\x22\x02\x00\x00\xD4\x00\x00'
          + b'\x00\x88\x01\x00\x00\xFF\xFF\xFF\xFF\x29\x02\x00\x00\x7D\x02\x00'
          + b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\xF3\x08\x41\xB2\x00\x00\xFF'
          + b'\xFF\x03\x00\x00\x00\x00\x00\x00\x00\xB6\x00\xFF\xFF\x01\x01\x00'
          + b'\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x03\x00\x00\x00\x05'
          + b'\x00\x00\x00\x07\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01'
          + b'\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\x02\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF'
          + b'\x00\x00\x00\x00\x4D\x45\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00'
          + b'\x00\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00'
          + b'\xDF\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF'
          + b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF'
          + b'\xFF\xFF\x01\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00'
          + b'\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00'
          + b'\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\x00\x00\x00\x00\x00\x00\xDF\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\xFE\xCA\x01\x00\x00\x00\xFF\xFF\xFF\xFF\x01'
          + b'\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\xFF\xFF\xFF'
          + b'\xFF\x00\x00')
    module1.addPerformanceCache(ca)

    project.addModule(thisWorkbook)
    project.addModule(sheet1)
    project.addModule(module1)

    assert stream.to_bytes() == decompressedStream

    # The compression results are not the same.
    compressed = ms_ovba.compress(stream.to_bytes())
    assert ms_ovba.decompress(compressed) == decompressedStream
