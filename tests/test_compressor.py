import pytest
from vbaProjectCompiler.decompressor import Compressor

def test_unableToCompress():
    comp = Compressor()
    input = "abcdefghijklmnopqrstuv."
    result = 
    expected = b'\x01\x19\xB0\x00\x61\x62\x63\x64\x65\x66\x67\x68\x00\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x00\x71\x72\x73\x74\x75\x76\x2E'
    assert comp.compress(input) == expected
