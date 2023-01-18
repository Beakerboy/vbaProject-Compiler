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
    #comp.setCompression(True)
    input = "abcdefghijklmnopqrstuv."
    #result = comp.compress(input);
    expected = b'\x01\x19\xB0\x00\x61\x62\x63\x64\x65\x66\x67\x68\x00\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x00\x71\x72\x73\x74\x75\x76\x2E'
    #assert expected == result

def test_maxCompression():
    comp = Decompressor()
    #comp.setCompression(True)
    #input = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    #result = comp.compress(input);
    expected = "\x01\x03\xB0\x02\x61\x45\x00"
    #assert expected == result

def test_normalCompression():
    comp = Decompressor()
    expected = "#aaabcdefaaaaghijaaaaaklaaamnopqaaaaaaaaaaaarstuvwxyzaaa"
    compressed = bytearray(b'\x2F\xB0\x00\x23\x61\x61\x61\x62\x63\x64\x65\x82\x66\x00\x70\x61\x67\x68\x69\x6A\x01\x38\x08\x61\x6B\x6C\x00\x30\x6D\x6E\x6F\x70\x06\x71\x02\x70\x04\x10\x72\x73\x74\x75\x76\x10\x77\x78\x79\x7A\x00\x3C')
    header = bytearray(compressed[:2])
    del compressed[:2]
    comp.setCompressedHeader(header)
    result = comp.decompress(compressed)
    assert expected == result

def test_compressRaw():
    comp = Decompressor()
    #comp.setCompression(False)
    #input = "a"
    #result = comp.compress(input);
    #header = bytearray(b'\xFF\x3F')
    #start = header + b'\x61'
    #expected = start.ljust(4095, b'\x00')
    #assert expected == result

def test_ChunkSizeMismatch():
    comp = Decompressor()
    header = b'\x19\xB0'
    comp.setCompressedHeader(header)
    data = b'\x00\x61\x62'
    with pytest.raises(Exception) as e_info:
        comp.setCompressedData(data)

def test_decompression():
    chunk = bytearray(b'\xA8\xB0\x00\x41\x74\x74\x72\x69\x62\x75\x74\x00\x65\x20\x56\x42\x5F\x4E\x61\x6D\x00\x65\x20\x3D\x20\x22\x53\x68\x65\x40\x65\x74\x31\x22\x0D\x0A\x0A\xE8\x42\x04\x61\x73\x02\x74\x30\x7B\x30\x30\x30\xC0\x32\x30\x38\x32\x30\x2D\x00\x20\x04\x08\x0E\x43\x00\x14\x02\x1C\x01\x24\x30\x30\x34\x36\x02\x7D\x0D\x7C\x47\x6C\x6F\x62\x61\x6C\x21\x01\xC4\x53\x70\x61\x63\x01\x92\x46\x61\x08\x6C\x73\x65\x0C\x64\x43\x72\x65\x61\x10\x74\x61\x62\x6C\x15\x1F\x50\x72\x65\x20\x64\x65\x63\x6C\x61\x00\x06\x49\x64\x11\x00\xAB\x54\x72\x75\x0D\x42\x45\x78\x70\x08\x6F\x73\x65\x14\x1C\x54\x65\x6D\x70\x00\x6C\x61\x74\x65\x44\x65\x72\x69\x06\x76\x02\x24\x92\x42\x75\x73\x74\x6F\x6D\x0C\x69\x7A\x04\x44\x03\x32')
    comp = Decompressor()
    comp.setCompressedHeader(chunk[:2])
    del chunk[:2]
    assert comp.compressedChunkSize == 171
    result = comp.decompress(chunk)
    expected = 'Attribute VB_Name = "Sheet1"\x0D\x0AAttribute VB_Base = "0{00020820-0000-000C0-020-000-000046}\x0D\x0AAttribute VB_Global'
    assert result == expected
    
def test_cielLog2():
    comp = Decompressor()
    assert comp.ceilLog2(1) == 4
    assert comp.ceilLog2(2) == 4
    assert comp.ceilLog2(3) == 4
    assert comp.ceilLog2(4) == 4
    assert comp.ceilLog2(9) == 4
    assert comp.ceilLog2(17) == 5
    assert comp.ceilLog2(50) == 6

def test_decompressUnableToCompressOneToken():
    compressed = bytearray(b'\x08\xB0\x00\x61\x62\x63\x64\x65\x66\x67\x68')
    comp = Decompressor()
    header = bytearray(compressed[:2])
    del compressed[:2]
    comp.setCompressedHeader(header)
    result = comp.decompress(compressed)
    expected = "abcdefgh"
    assert expected == result

def test_zeroTokens():
    compressed = bytearray(b'\x00\xB0\x00')
    comp = Decompressor()
    header = bytearray(compressed[:2])
    del compressed[:2]
    comp.setCompressedHeader(header)
    with pytest.raises(Exception) as e_info:
        result = comp.decompress(compressed)
    
def test_decompressUnableToCompressOneToken():
    compressed = bytearray(b'\x19\xB0\x00\x61\x62\x63\x64\x65\x66\x67\x68\x00\x69\x6A\x6B\x6C\x6D\x6E\x6F\x70\x00\x71\x72\x73\x74\x75\x76\x2E')
    comp = Decompressor()
    header = bytearray(compressed[:2])
    del compressed[:2]
    comp.setCompressedHeader(header)
    result = comp.decompress(compressed)
    expected = "abcdefghijklmnopqrstuv."
    assert expected == result

def test_CopytokenHelp():
    comp = Decompressor()
    comp.uncompressedData = 'Attribute VB_Name = "Sheet1"\x0D\x0A'
    result = comp.copytokenHelp()
    assert result["bitCount"] == 5
    assert result["lengthMask"] == 0x07FF
    assert result["offsetMask"] == 0xF800
    tokenData = comp.unpackCopytoken(0xE80A)
    assert tokenData["length"] == 13
    assert tokenData["offset"] == 30

def test_Copytoken1():
    comp = Decompressor()
    comp.uncompressedData = '#aaabcdef'
    result = comp.copytokenHelp()
    assert result["bitCount"] == 4
    assert result["lengthMask"] == 0x0FFF
    assert result["offsetMask"] == 0xF000
    tokenData = comp.unpackCopytoken(0x7000)
    assert tokenData["length"] == 3
    assert tokenData["offset"] == 8

    comp.uncompressedData = '#aaabcdefaaaaghij'
    result = comp.copytokenHelp()
    assert result["bitCount"] == 5
    assert result["lengthMask"] == 0x07FF
    assert result["offsetMask"] == 0xF800
    tokenData = comp.unpackCopytoken(0x3801)
    assert tokenData["length"] == 4
    assert tokenData["offset"] == 8

    comp.uncompressedData = '#aaabcdefaaaaghijaaaaakl'
    result = comp.copytokenHelp()
    tokenData = comp.unpackCopytoken(0x3000)
    assert tokenData["length"] == 3
    assert tokenData["offset"] == 7

    comp.uncompressedData = '#aaabcdefaaaaghijaaaaaklaaamnopq'
    result = comp.copytokenHelp()
    tokenData = comp.unpackCopytoken(0x7002)
    assert tokenData["length"] == 5
    assert tokenData["offset"] == 15

    comp.uncompressedData = '#aaabcdefaaaaghijaaaaaklaaamnopqaaaaa'
    result = comp.copytokenHelp()
    tokenData = comp.unpackCopytoken(0x1004)
    assert tokenData["length"] == 7
    assert tokenData["offset"] == 5
