import pytest
from vbaProjectCompiler.FileIO.miniChain import MiniChain


def test_getSectorSize():
    chain = MiniChain(64)
    assert chain.getSectorSize() == 64


def test_zeroLength():
    chain = MiniChain(64)
    assert len(chain) == 0


def test_addStream()
    chain = MiniChain(64)
    stream = StreamStub(16)
    chain.addStream(stream)
    assert len(chain) == 1


def test_addBiggerData():
    chain = MiniChain(64)
    stream = StreamStub(65)
    chain.addStream(stream)
    assert len(chain) == 2


class StreamStub(StreamBase):
    def __init__(self, size):
        super().__init__()
        self._mocksize = size

    def getSize(self):
        return self._mocksize
