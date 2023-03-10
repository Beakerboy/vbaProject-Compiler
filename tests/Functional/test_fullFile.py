import struct
import unittest.mock
import uuid
from ms_ovba_compression.ms_ovba import MsOvba
from ms_pcode_assembler.module_cache import ModuleCache
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Models.Entities.doc_module import DocModule
from vbaProjectCompiler.Models.Entities.std_module import StdModule
from vbaProjectCompiler.Models.Entities.referenceRecord import ReferenceRecord
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference


class NotSoRandom():
    _rand = []

    @classmethod
    def set_seed(cls, seeds):
        cls._rand = seeds

    @classmethod
    def randint(cls, param1, param2):
        return cls._rand.pop(0)


def module_matches_bin(module_path,
                       cache_size,
                       bin_path,
                       bin_offset,
                       bin_length):
    m = open(module_path, "rb")
    b = open(bin_path, "rb")
    b.seek(bin_offset)
    if m.read(cache_size) != b.read(cache_size):
        return False
    ms_ovba = MsOvba()
    m_uncompressed = ms_ovba.decompress(m.read())
    b_uncompressed = ms_ovba.decompress(b.read(bin_length))
    return m_uncompressed == b_uncompressed


@unittest.mock.patch('random.randint', NotSoRandom.randint)
def test_fullFile():
    rand = [0x41, 0xBC, 0x7B, 0x7B, 0x37, 0x7B, 0x7B, 0x7B]
    NotSoRandom.set_seed(rand)
    project = VbaProject()
    codePage = 0x04E4
    codePageName = "cp" + str(codePage)
    libidRef = LibidReference(
        uuid.UUID("0002043000000000C000000000000046"),
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
    libidRef2 = LibidReference(
        uuid.UUID("2DF8D04C5BFA101BBDE500AA0044DE52"),
        "2.0",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    )
    officeReference = ReferenceRecord(codePageName, "Office", libidRef2)
    project.addReference(oleReference)
    project.addReference(officeReference)
    project.setProjectCookie(0x08F3)
    project.setProjectId('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    project.setPerformanceCache(createCache())
    project.setPerformanceCacheVersion(0x00B5)

    module_cache = ModuleCache(0xB5, 0x08F3)
    module_cache.misc = [0x0316, 0x0123, 0x88, 8, 0x18, "00000000", 1]
    indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                      "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                      "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                      "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
    module_cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
    object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                    "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                    "02 3C FF FF FF FF 00 00")
    module_cache.object_table = bytes.fromhex(" ".join(object_table))

    # Add Modules
    this_workbook = DocModule("ThisWorkbook")
    this_workbook.cookie.value = 0xB81C
    module_cache.module_cookie = 0xB81C
    guid = uuid.UUID("0002081900000000C000000000000046")
    module_cache.guid = bytes(("0{" + str(guid) + "}").upper(), "utf_16_le")
    this_workbook.set_guid(guid)
    module_path = "vbaProjectCompiler/blank_files/ThisWorkbook.cls"
    this_workbook.add_file(module_path)
    this_workbook.normalize_file()
    this_workbook.set_cache(module_cache.to_bytes())

    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    module_cache.module_cookie = 0x9B9A
    guid = uuid.UUID("0002082000000000C000000000000046")
    module_cache.guid = bytes(("0{" + str(guid) + "}").upper(), "utf_16_le")
    sheet1.set_guid(guid)
    module_path = "vbaProjectCompiler/blank_files/Sheet1.cls"
    sheet1.add_file(module_path)
    sheet1.normalize_file()
    sheet1.set_cache(module_cache.to_bytes())

    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    module_cache.clear_variables()
    module_cache.misc = [0x0316, 3, 0, 2, 0xFFFF, "FFFFFFFF", 0]
    module_cache.indirect_table = struct.pack("<iI", -1, 0x78)
    module_cache.module_cookie = 0xB241
    module1.addWorkspace(26, 26, 1349, 522, 'Z')
    module_path = "tests/blank/Module1.bas"
    module1.add_file(module_path)
    module1.normalize_file()
    module1.set_cache(module_cache.to_bytes())

    project.addModule(this_workbook)
    project.addModule(sheet1)
    project.addModule(module1)

    project.write_file()
    path = "vbaProjectCompiler/blank_files/ThisWorkbook.cls.bin"
    assert module_matches_bin(path, 0x0333,
                              "tests/blank/vbaProject.bin", 0x0800, 0xB5)
    path = "vbaProjectCompiler/blank_files/Sheet1.cls.bin"
    assert module_matches_bin(path, 0x0333, "tests/blank/vbaProject.bin",
                              0x0C00, 0xAC)

    # fileIO = OleFile(project)
    # fileIO.build_file()

    # Alter red-black tree
    # fileIO.streams[2].color = 1
    # fileIO.streams[3].color = 1
    # fileIO.streams[4].color = 1
    # fileIO.streams[8].color = 1

    # fileIO.write_file(".")
    # assert size of ./vbaProject.bin == size of tests/blank.vbaProject.bin
    # compare new file to blank file in 512 block chunks
    # new = open("./vbaProject.bin", "rb")
    # expected = open("tests/blank/vbaProject.bin", "rb")
    # for chunk in iter(partial(new.read, 512), ''):
    #   assert chunk == expected.read(512)


def createCache():
    vbaProject = VbaProject()
    vbaProject.setPerformanceCacheVersion(0x00B5)
    thisWorkbook = DocModule("ThisWorkbook")
    thisWorkbook.cookie.value = 0xB81C
    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241

    libraries = []
    delim = []
    libraries.append(LibidReference(
        "{000204EF-0000-0000-C000-000000000046}",
        "4.2",
        "9",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\VBA"
        "\\VBA7.1\\VBE7.DLL",
        "Visual Basic For Applications"
    ))
    delim.append(0x011A)
    libraries.append(LibidReference(
        "{00020813-0000-0000-C000-000000000046}",
        "1.9",
        "0",
        "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "Microsoft Excel 16.0 Object Library"
    ))
    delim.append(0x00BC)
    libraries.append(LibidReference(
        "{00020430-0000-0000-C000-000000000046}",
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    ))
    delim.append(0x0128)
    libraries.append(LibidReference(
        "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
        "2.8",
        "0",
        "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
        "Microsoft Office 16.0 Object Library"
    ))
    delim.append(0x0003)
    ca = (b''
          + b'\xFF\x09\x04\x00\x00\x09\x04\x00\x00\xE4\x04\x03\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x01\x00\x04\x00\x02\x00\x20\x01')
    i = 0
    for lib in libraries:
        ca += bytearray(str(lib), "utf_16_le")
        ca += struct.pack("<IIIH", 0, 0, 0, delim[i])
        i += 1
    ca += struct.pack("<17H", 2, 2, 1, 6, 0x0212, 0, 0x0214, 1, 0x0216, 1,
                      0x0218, 0, 0x021a, 1, 0x021c, 1, 0x0222)
    ca += b'\xFF' * 6 + b'\x00' * 4 + b'\xFF' * 36
    prefix = [0x0018, 0x000C, 0x000E]
    # index = 0x0046
    i = 0

    for module in vbaProject.modules:
        name = module.modName.value.encode("utf_16_le")
        ca += struct.pack("<H", prefix[i]) + name
        ca += struct.pack("<HH", 0x0014, 0x0032) + chr(69 + i)
        ca += "65be0257".encode("utf_16_le")
        ca += struct.pack("<HHH", 0xFFFF, 0x0227, prefix[i])
        ca += name + struct.pack("<HHHI", 0xFFFF, module.cookie.value, 0, 0)
        i += 1
    return ca
