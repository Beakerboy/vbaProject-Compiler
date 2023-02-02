import pytest
from vbaProjectCompiler.Helpers.compressor import Compressor

def test_unableToCompress():
    input = b'abcdefghijklmnopqrstuv.'
    comp = Compressor(input)
    expected = b'\x01\x19\xB0\x00\x61\x62\x63\x64\x65\x66\x67\x68\x00\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x00\x71\x72\x73\x74\x75\x76\x2E'
    assert comp.compress() == expected

def test_maxCompression():
    input = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    comp = Compressor(input)
    expected = "\x01\x03\xB0\x02\x61\x45\x00"
    assert comp.compress() == expected
