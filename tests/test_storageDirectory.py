import pytest
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory
from vbaProjectCompiler.Directories.storageDirectory import StorageDirectory

def test_StorageDirectory():
    #why is this not cleaned up? Need to used dir1 for some reason
    dir1 = StorageDirectory()
    assert dir1.type == 1
    assert len(dir1.directories) == 0
    assert dir1.minifatSectorsUsed() == 0

def test_addFile():
    dir2 = StorageDirectory()
    stream = StreamDirectory()
    stream.filePath = "tests/blank/PROJECT"
    dir2.addFile(stream)
    assert dir2.minifatSectorsUsed() == 7
    assert dir2.fileSize() == 0
