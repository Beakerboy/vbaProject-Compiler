import pytest
from vbaProjectCompiler.FileIO.miniChain import MiniChain
from vbaProjectCompiler.FileIO.sectorChain import SectorChain
from vbaProjectCompiler.Models.Entities.Streams.streamBase import StreamBase


def test_getSectorSize():
    chain = MiniChain(64)
    assert chain.getSectorSize() == 64


def test_zeroLength():
    chain = MiniChain(64)
    assert len(chain) == 0


def test_addSmallStream():
    chain = MiniChain(64)
    stream = StreamStub(16)
    parentChain = ChainMock(512)
    chain.setStorageChain(parentChain)
    parentChain.addStream(chain)
    chain.addStream(stream)
    assert len(chain) == 1


def test_parentChain():
    chain = MiniChain(64)
    stream = StreamStub(16)
    parentChain = ChainMock(512)
    chain.setStorageChain(parentChain)
    parentChain.addStream(chain)
    assert chain.getStartSector() == 0 


def test_addBiggerData():
    chain = MiniChain(64)
    stream = StreamStub(65)
    parentChain = ChainMock(512)
    chain.setStorageChain(parentChain)
    chain.setStorageChain(parentChain)
    chain.setStartSector(0)  # Shuldn't have to do this (again?)
    chain.addStream(stream)
    assert len(chain) == 2


class ChainMock(SectorChain):
    pass


class StreamStub(StreamBase):
    def __init__(self, size):
        super().__init__()
        self._mocksize = size

    def streamSize(self):
        return self._mocksize
