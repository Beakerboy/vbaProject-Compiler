from functools import partial

test_fullFile():
    project = VbaProject()
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
    project.setProjectId('{9E394C0B-697E-4AEE-9FA6-446F51FB30DC}')
    project.setProtectionState("41435A5A5E5A5E5A5E5A5E")
    project.setPassword("BCBEA7A2591C5A1C5A1C")
    project.setVisibilityState("37352C2BDCDD56DE56DEA9")
    #project.setPerformanceCache(b'')
    project.setPerformanceCacheVersion(0x00B5)

    # Add Modules
    thisWorkbook = DocModule("ThisWorkbook")
    thisWorkbook.cookie.value = 0xB81C
    cache = b'\x01\x16\x03\x00\x00\xF0\x00\x00\x00\xD2\x02\x00\x00\xD4\x00\x00\x00\x00\x02\x00\x00\xFF\xFF\xFF\xFF\xD9\x02\x00\x00\x2D\x03\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xF3\x08\x1C\xB8\x00\x00\xFF\xFF\x23\x01\x00\x00\x88\x00\x00\x00\xB6\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x4D\x45\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\xDF\x00\xFF\xFF\x00\x00\x00\x00\x18\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x28\x00\x00\x00\x02\x00\x53\x4C\xFF\xFF\xFF\xFF\x00\x00\x01\x00\x53\x10\xFF\xFF\xFF\xFF\x00\x00\x01\x00\x53\x94\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x02\x3C\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\x01\x00\x4E\x00\x30\x00\x7B\x00\x30\x00\x30\x00\x30\x00\x32\x00\x30\x00\x38\x00\x31\x00\x39\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x2D\x00\x43\x00\x30\x00\x30\x00\x30\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x34\x00\x36\x00\x7D\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01\x40\x00\x00\x00\x02\x80\xFE\xFF\xFF\xFF\xFF\xFF\x20\x00\x00\x00\xFF\xFF\xFF\xFF\x30\x00\x00\x00\x02\x01\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x2E\x00\x43\x00\x1D\x00\x00\x00\x25\x00\x00\x00\xFF\xFF\xFF\xFF\x40\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\xDF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFE\xCA\x01\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00'
    thisWorkbook.addPerformanceCache(cache)
    #thisWorkbook.addFile(path)

    sheet1 = DocModule("Sheet1")
    sheet1.cookie.value = 0x9B9A
    sheet1.addPerformanceCache(cache)
    #sheet1.addFile(path)

    module1 = StdModule("Module1")
    module1.cookie.value = 0xB241
    cache = b'\x01\x16\x03\x00\x00\xF0\x00\x00\x00\x22\x02\x00\x00\xD4\x00\x00\x00\x88\x01\x00\x00\xFF\xFF\xFF\xFF\x29\x02\x00\x00\x7D\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xF3\x08\x41\xB2\x00\x00\xFF\xFF\x03\x00\x00\x00\x00\x00\x00\x00\xB6\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x4D\x45\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\xDF\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\xDF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFE\xCA\x01\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00'
    module1.addPerformanceCache(cache)
    module1.addWorkspace(26, 26, 1349, 522, 'Z')
    #module1.addFile(path)

    project.addModule(thisWorkbook)
    project.addModule(sheet1)
    project.addModule(module1)
    fileIO = FileIO(project)
    fileIO.writeFile(".")
    assert size of ./vbaProject.bin == size of tests/blank.vbaProject.bin
    # compare new file to blank file in 512 block chunks
    new = open(./vbaProject.bin, "rb")
    expected = open("tests/blank/vbaProject.bin", "rb")
    for chunk in iter(partial(new.read, 512), ''):
        assert chunk == expected.read(512)
