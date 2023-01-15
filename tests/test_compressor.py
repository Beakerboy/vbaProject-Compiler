import pytest
from vbaProjectCompiler.decompressor import Decompressor

def test_Compressor():
    comp = Decompressor()
    header = b'\x19\xB0'
    comp.setCompressedHeader(header)
    expected = 28
    result = comp.getCompressedChunkSize()
    assert expected == result
    data = b'\x00\x61\x62\x63\x64\x65\x66\x67\x68\x00\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x00\x71\x72\x73\x74\x75\x76\x2E'
    comp.setCompressedData(data)
    assert comp.getCompressedChunk() == bytearray(header) + bytearray(data)

def test_unableToCompress():
    comp = Decompressor()
    comp.setCompression(True)
    input = "abcdefghijklmnopqrstuv."
    result = comp.compress(input);
    expected = b'\x01\x19\xB0\x00\x61\c62\x63\x64\x65\x66\x67\x68\x00\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x00\x71\x72\x73\x74\x75\x76\x2E'
    #assert expected == result

def test_maxCompression():
    comp = Decompressor()
    comp.setCompression(True)
    input = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    result = comp.compress(input);
    expected = "\x01\x03\xB0\x02\x61\x45\x00"
    #assert expected == result

def test_normalCompression():
    comp = Decompressor()
    comp.setCompression(True)
    input = "#aaabcdefaaaaghijaaaaaklaaamnopqaaaaaaaaaaaarstuvwxyzaaa"
    result = comp.compress(input);
    expected = b'\x01\x2F\xB0\x00\x23\x61\x61\x61\x62\x63\x64\x65\x82\x66\x00\x70\x61\x67\x68\x69\x6A\x01\x38\x08\x61\x6B\x6C\x00\x30\x6D\x6E\x6F\x70\x06\x71\x02\x70\x04\x10\x72\x73\x74\x75\x76\x10\x77\x78\x79\x7A\x00\x3C' 
    #assert expected == result

def test_compressRaw():
    comp = Decompressor()
    comp.setCompression(False)
    input = "a"
    result = comp.compress(input);
    header = bytearray(b'\xFF\x3F')
    start = header + b'\61'
    expected = start.ljust(4095, b'\x00')
    assert expected == result
