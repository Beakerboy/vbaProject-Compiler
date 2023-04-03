import uuid
from vbaProjectCompiler.Models.Fields.libid_reference import LibidReference


def test_str() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    libid_ref = LibidReference(
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    expected = ("*\\G{00020430-0000-0000-C000-000000000046}"
                "#2.0#0#C:\\Windows\\System32\\stdole2.tlb#OLE Automation")
    assert str(libid_ref) == expected
    assert len(libid_ref) == 94


def test_posix() -> None:
    guid = uuid.UUID('0002043000000000C000000000000046')
    libid_ref = LibidReference(
        guid,
        "2.0",
        "0",
        "//usr/bin/stdole2.tlb",
        "OLE Automation"
    )
    expected = ("*\\H{00020430-0000-0000-C000-000000000046}"
                "#2.0#0#//usr/bin/stdole2.tlb#OLE Automation")
    assert str(libid_ref) == expected
