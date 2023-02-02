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
    expected = b'\x01\x03\xB0\x02\x61\x45\x00'
    assert comp.compress() == expected

def test_normalCompresson():
    input = b'#aaabcdefaaaaghijaaaaaklaaamnopqaaaaaaaaaaaarstuvwxyzaaa'
    comp = Compressor(input)
    expected = bytearray(b'\x01\x2F\xB0\x00\x23\x61\x61\x61\x62\x63\x64\x65\x82\x66\x00\x70\x61\x67\x68\x69\x6A\x01\x38\x08\x61\x6B\x6C\x00\x30\x6D\x6E\x6F\x70\x06\x71\x02\x70\x04\x10\x72\x73\x74\x75\x76\x10\x77\x78\x79\x7A\x00\x3C')
    assert comp.compress() == expected
