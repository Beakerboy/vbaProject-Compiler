import struct
import uuid
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.dirStream import DirStream
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference
from vbaProjectCompiler.Models.Entities.doc_module import DocModule
from vbaProjectCompiler.Models.Entities.std_module import StdModule
from vbaProjectCompiler.Models.Entities.referenceRecord import ReferenceRecord


def test_dirstream() -> None:
    module_cache = ModuleCache(0xB5, 0x08F3)
    # Read the data from the demo file and decompress it.
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x1EC0
    length = 0x0232
    f.seek(offset)
    container = f.read(length)
    ms_ovba = MsOvba()
    decompressed_stream = ms_ovba.decompress(container)

    # Create a project with the same attributes
    project = VbaProject()
    stream = DirStream(project)
    codepage = 0x04E4
    codepage_name = "cp" + str(codepage)
    guid = uuid.UUID('0002043000000000C000000000000046')
    libid_ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    ole_reference = ReferenceRecord(codepage_name, "stdole", libid_ref)
    guid = uuid.UUID('2DF8D04C5BFA101BBDE500AA0044DE52')
    libid_ref2 = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )
    office_reference = ReferenceRecord(codepage_name, "Office", libid_ref2)
    project.addReference(ole_reference)
    project.addReference(office_reference)
    project.set_project_cookie(0x08F3)

    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    module_cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                    "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                    "02 3C FF FF FF FF 00 00")
    module_cache.object_table = bytes.fromhex(" ".join(object_table))
    module_cache.misc = [0x0316, 0x0123, 0x88, 8,
                         0x18, "00000000", 1]

    this_workbook = DocModule("ThisWorkbook")
    this_workbook.cookie.value = 0xB81C
    module_cache.cookie = this_workbook.cookie.value
    guid = uuid.UUID('0002081900000000C000000000000046')
    this_workbook.set_guid(guid)
    module_cache.guid = [guid]
    this_workbook.set_cache(module_cache.to_bytes())

    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    module_cache.cookie = sheet1.cookie.value
    guid = uuid.UUID('0002082000000000C000000000000046')
    module_cache.guid = [guid]
    sheet1.set_guid(guid)
    sheet1.set_cache(module_cache.to_bytes())

    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    module_cache.clear_variables()
    module_cache.cookie = module1.cookie.value
    module_cache.misc = [0x0316, 3, 0, 2,
                         0xFFFF, "FFFFFFFF", 0]
    module_cache.indirect_table = struct.pack("<iI", -1, 0x78)
    module1.set_cache(module_cache.to_bytes())

    project.addModule(this_workbook)
    project.addModule(sheet1)
    project.addModule(module1)

    assert stream.to_bytes() == decompressed_stream

    # The compression results are not the same.
    compressed = ms_ovba.compress(stream.to_bytes())
    assert ms_ovba.decompress(compressed) == decompressed_stream
