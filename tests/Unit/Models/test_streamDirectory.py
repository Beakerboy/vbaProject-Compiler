from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory


def test_StreamDirectory():
    stub = ModeStub()
    dir = StreamDirectory.createFromModule(stub)
    assert dir.type == 2


class ModuleStub():

    def __init__(self):
        self.name = "stub"
