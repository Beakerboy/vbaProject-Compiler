from vbaProjectCompiler.Directories.rootDirectory import RootDirectory


def test_RootDirectory():
    dir = RootDirectory()
    assert dir.type == 5
    stream = StreamDirectory()
    stream.filePath = "tests/blank/PROJECT"
    dir.addFile(stream)
    assert dir.fileSize() == 448
