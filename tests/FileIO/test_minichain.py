import pytest
from vbaProjectCompiler.FileIO.miniChain import MiniChain

def test_addData():
    chain = MiniChain(64)
    sectors = chain.addData(b'\x00')
    assert sectors == [0]
