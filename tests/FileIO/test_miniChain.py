import pytest
from vbaProjectCompiler.FileIO.miniChain import MiniChain

def test_addData():
    chain = MiniChain(64)
    sectors = chain.addStream(b'\x00')
    assert sectors == [0]
