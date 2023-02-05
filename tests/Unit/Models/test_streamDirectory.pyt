from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory


def test_StreamDirectory():
    dir = StreamDirectory()
    assert dir.type == 2
    dir.filePath = "tests/blank/PROJECT"
    assert dir.minifatSectorsUsed() == 7
    assert dir.fileSize() == 447
