import pytest
from vbaProjectCompiler.FileIO.miniChain import MiniChain

def test_addData():
    chain = MiniChain(64)
    sectors = chain.addStream(b'\x00')
    assert sectors == [0]

def test_addBiggerData():
    chain = MiniChain(64)
    f = open("tests/blank/ThisWorkbook", "rb")
    data = f.read()
    sectors = chain.addStream(data)
    assert len(sectors) == 5
