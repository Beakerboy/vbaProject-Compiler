# test_fatChain.py

import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.FileIO.fatChain import FatChain
from vbaProjectCompiler.Directories.directory import Directory

def test_initialProperties():
    chain = FatChain(512)
    assert chain.getLength() == 1
    assert chain.getChain() == [0xfffffffd]

def test_addingChain():
    chain = FatChain(512)
    chain.startNewChain()
    assert chain.getLength() == 2
    assert chain.getChain() == [0xfffffffd, 0xfffffffe]

    chain.startNewChain()
    assert chain.getLength() == 3
    assert chain.getChain() == [0xfffffffd, 0xfffffffe, 0xfffffffe]

def test_extendChain():
    chain = FatChain(512)
    chain.startNewChain()
    chain.startNewChain()
    chain.extendChain(1, 2)
    assert chain.getLength() == 5
    assert chain.getChain() == [0xfffffffd, 3, 0xfffffffe, 4, 0xfffffffe]

def test_zeroLengthException():
    chain = FatChain(512)
    chain.startNewChain()
    
    with pytest.raises(Exception) as e_info:
        chain.extendChain(1, 0)

def test_tooShortException():
    chain = FatChain(512)
    chain.startNewChain()
    
    with pytest.raises(Exception) as e_info:
        chain.extendChain(4, 4)

def test_newFatTableSector():
    chain = FatChain(512)
    chain.startNewChain()
    chain.extendChain(0, 127)
    chain.startNewChain()
    assert assert chain.getLength() == 130
