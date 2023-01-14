import pytest
from vbaProjectCompiler.decompressor import Decompressor

def test_Compressor():
    comp = Decompressor()
    comp.setCompressedHeader(b'\x16\x03')
    expected = 355
    result = comp.getCompressedChunkSize()
    assert expected == result
