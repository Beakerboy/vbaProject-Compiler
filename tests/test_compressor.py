import pytest
from vbaProjectCompiler.decompressor import Decompressor

def test_Compressor():
    comp = Decompressor()
    comp.setCompressedHeader(b'0x1603')
    expected = 355
    result = comp.getCompressedChunkSize()
    assert expected == result
