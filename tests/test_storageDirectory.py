import pytest
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory
from vbaProjectCompiler.Directories.storageDirectory import StorageDirectory


def test_StorageDirectory():
    dir1 = StorageDirectory()
    assert dir1.type == 1
    assert len(dir1.directories) == 0

    class MockField:
        value = "foo"

    class MockModule():
        type = 2
        modName = MockField()

    mock = MockModule()
    assert len(dir1.flatten()) == 1
    dir1.addModule(mock)
    assert len(dir1.flatten()) == 2
