# test_vbaProjectCompiler.py

import pytest
from vbaProjectCompiler.Directories.directory import Directory
from vbaProjectCompiler.Directories.rootDirectory import RootDirectory
from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory
from vbaProjectCompiler.Directories.storageDirectory import StorageDirectory

def test_directory():

    dir = RootDirectory()
    dir.name = "Root Entry"
    assert dir.nameSize() == 22

    dir.subDirectoryId = 8
    dir.modifiedHigh = 3266847680
    dir.modifiedLow  =   31007795
    dir.sector = 3

    expected = b'\x52\x00\x6F\x00\x6F\x00\x74\x00\x20\x00\x45\x00\x6E\x00\x74\x00\x72\x00\x79\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x00\x05\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0\x23\xB8\xC2\x33\x24\xD9\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    result = dir.writeDirectory()
    assert result == expected
    
def test_RootDirectory():
    dir = RootDirectory()
    assert dir.type == 5
    stream = StreamDirectory()
    stream.filePath = "tests/blank/PROJECT"
    dir.addFile(stream)
    assert dir.fileSize() == 384

def test_StorageDirectory():
    dir = StorageDirectory()
    assert dir.type == 1
    assert dir.directories[0].filePath == ""
    assert len(dir.directories) == 0
    assert dir.minifatSectorsUsed() == 0

def test_addFile():
    dir = StorageDirectory()
    stream = StreamDirectory()
    stream.filePath = "tests/blank/PROJECT"
    dir.addFile(stream)
    assert dir.minifatSectorsUsed() == 6
    assert dir.fileSize() == 0

def test_StreamDirectory():
    dir = StreamDirectory()
    assert dir.type == 2
    dir.filePath = "tests/blank/PROJECT"
    assert dir.minifatSectorsUsed() == 6
    assert dir.fileSize() == 323
