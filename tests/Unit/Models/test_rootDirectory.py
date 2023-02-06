import pytest
from vbaProjectCompiler.Directories.rootDirectory import RootDirectory


def test_directory():

    dir = RootDirectory()
    dir.name = "Root Entry"
    assert dir.nameSize() == 22

    dir.subDirectoryId = 8
    dir.modified = 0x01D92433C2B823C0
    dir.setStartSector(3)

    ex = (b''
          + b'\x52\x00\x6F\x00\x6F\x00\x74\x00\x20\x00\x45\x00\x6E\x00\x74\x00'
          + b'\x72\x00\x79\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x16\x00\x05\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x08\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0\x23\xB8\xC2'
          + b'\x33\x24\xD9\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
         )

    assert dir.writeDirectory('cp1254', 'little') == ex


def test_RootDirectory():
    dir = RootDirectory()
    assert dir.type == 5

    class StreamMock():
        def minifatSectorsUsed(self):
            return 4

    mock = StreamMock()
    
    dir.addFile(mock)
    assert dir.fileSize() == 256
