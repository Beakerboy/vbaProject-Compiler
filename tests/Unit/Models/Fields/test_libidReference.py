from vbaProjectCompiler.Models.Fields.libidReference import LibidReference


def test_str():
    libidRef = LibidReference(
        "windows",
        "{00020430-0000-0000-C000-000000000046}",
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    expected = ("*\G{00020430-0000-0000-C000-000000000046}"
                "#2.0#0#C:\Windows\System32\stdole2.tlb#OLE Automation")
    assert srt(libidRef) == expected
    assert len(libidRef) == 93
