import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Directories.directory import Directory
from vbaProjectCompiler.FileIO.fatChain import FatChain
from vbaProjectCompiler.Models.Entities.Streams.streamBase import StreamBase


def test_initialProperties():
    chain = FatChain(512)
    assert chain.getSectorSize() == 512
    assert len(chain) == 1
    assert chain.getChain() == [0xfffffffd]


def test_addingChain():
    chain = FatChain(512)
    stream = StreamStub()
    chain.addStream(stream)
    assert len(chain) == 2
    assert chain.getChain() == [0xfffffffd, 0xfffffffe]

    stream2 = StreamStub()
    chain.addStream(stream2)
    assert len(chain) == 3
    assert chain.getChain() == [0xfffffffd, 0xfffffffe, 0xfffffffe]


def test_extendChain():
    chain = FatChain(512)
    stream1 = StreamStub()
    chain.addStream(stream1)
    stream2 = StreamStub()
    chain.addStream(stream2)
    chain.extendChain(stream1, 2)
    assert len(chain) == 5
    assert chain.getChain() == [0xfffffffd, 3, 0xfffffffe, 4, 0xfffffffe]


def test_newFatTableSector():
    chain = FatChain(512)
    stream1 = StreamStub()
    chain.addStream(stream1)
    chain.extendChain(stream1, 126)
    stream2 = StreamStub()
    chain.addStream(stream2)
    assert chain.getChain()[126:] == [127, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_extendThroughFatSector():
    chain = FatChain(512)
    stream1 = StreamStub()
    chain.addStream(stream1)
    chain.extendChain(stream1, 126)
    assert len(chain) == 128

    chain.extendChain(stream1, 1)
    assert chain.getChain()[126:] == [127, 129, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_lastSectorOnFatSector():
    chain = FatChain(512)
    stream1 = StreamStub()
    chain.addStream(stream1)
    chain.extendChain(stream1, 125)
    assert len(chain) == 127
    chain.extendChain(stream1, 2)
    assert chain.getChain()[126:] == [127, 129, 0xFFFFFFFD, 0xFFFFFFFE]
    assert len(chain) == 130


def test_extendThroughFatSector2():
    chain = FatChain(512)
    stream1 = StreamStub()
    chain.addStream(stream1)
    chain.extendChain(stream1, 125)
    chain.extendChain(stream1, 3)
    assert len(chain) == 131
    assert chain.getChain()[126:] == [127, 129, 0xFFFFFFFD, 130,0xFFFFFFFE]


class StreamStub(StreamBase):
    def streamSize(self):
        return 1
