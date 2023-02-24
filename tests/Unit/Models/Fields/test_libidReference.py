import uuid
from vbaProjectCompiler.Models.Fields.libidReference import LibidReference


def test_str():
    guid = uuid.UUID('0002043000000000C000000000000046')
    libidRef = LibidReference(
        "windows",
        guid,
        "2.0",
        "0",
        "C:\\Windows\\System32\\stdole2.tlb",
        "OLE Automation"
    )
    expected = ("*\\G{00020430-0000-0000-C000-000000000046}"
                "#2.0#0#C:\\Windows\\System32\\stdole2.tlb#OLE Automation")
    assert str(libidRef) == expected
    assert len(libidRef) == 94
