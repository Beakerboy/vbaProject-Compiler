import uuid
from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.dirStream import DirStream
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
from vbaProjectCompiler.Models.Entities.doc_module import DocModule
from vbaProjectCompiler.Models.Entities.std_module import StdModule
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
    guid = uuid.UUID('0002043000000000C000000000000046')
    libidRef = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
    guid = uuid.UUID('2DF8D04C5BFA101BBDE500AA0044DE52')
    libidRef2 = LibidReference(
        guid,
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
    guid = uuid.UUID('0002081900000000C000000000000046')
    thisWorkbook.set_guid(guid)
    thisWorkbook.create_cache()

    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    guid = uuid.UUID('0002082000000000C000000000000046')
    sheet1.set_guid(guid)
    sheet1.create_cache()

    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    module1.create_cache()

    project.addModule(thisWorkbook)
    project.addModule(sheet1)
    project.addModule(module1)

    assert stream.to_bytes() == decompressedStream

    # The compression results are not the same.
    compressed = ms_ovba.compress(stream.to_bytes())
    assert ms_ovba.decompress(compressed) == decompressedStream
