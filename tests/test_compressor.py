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
    expected = 'Attribute VB_Name = "Sheet1"\x0D\x0AAttribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"\x0D\x0AAttribute VB_GlobalNameSpace = False\x0D\x0AAttribute VB_Creatable = False\x0D\x0AAttribute VB_PredeclaredId = True\x0D\x0AAttribute VB_Exposed = True\x0D\x0AAttribute VB_TemplateDerived = False\x0D\x0AAttribute VB_Customizable = True\x0D\x0A'
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

def test_dir():
    chunk = bytearray(b'\x2E\xB2\x80\x01\x00\x04\x00\x00\x00\x03\x00\x30\xAA\x4A\x06eam\x90\x02\x02\x48\x09\x00\xC0\x14\x06\x48\x08\x03\x00\x02\x00\x8C\xE4\x04\x04\x00\x02\x0A\x00\x1C\x56\x42\x41\x50\x72\x6F\x20\x6A\x65\x63\x74\x05\x00\x1A\x00\x00\xAA\x40\x02\x0A\x06\x02\x0A\x3D\x02\x0A\x07\x02\x72\x15\x01\x14\x08\x06\x12\x09\x02\x12\x57\x02\xBE\x50\x65\x11\x00\x0C\x02\x4A\x3C\x02\x0A\x16\x02\x00\x01\x39\x73\x74\x64\x6F\x6C\x65\x02\x3E\x02\x19\x73\x00\x74\x00\x64\x00\x00\x6F\x00\x6C\x00\x65\x00\x0D\x00\x0A\x68\x00\x25\x5E\x00\x03\x2A\x5C\x47\x7B\x00\x30\x30\x30\x32\x30\x34\x33\x30\x76\x2D\x00\x08\x04\x04\x43\x00\x0A\x02\x0E\x01\x12\x30\x00\x30\x34\x36\x7D\x23\x32\x2E\x30\x00\x23\x30\x23\x43\x3A\x5C\x57\x69\x00\x6E\x64\x6F\x77\x73\x5C\x53\x79\x80\x73\x74\x65\x6D\x33\x32\x5C\x03\x65\x00\x32\x2E\x74\x6C\x62\x23\x4F\x4C\x00\x45\x20\x41\x75\x74\x6F\x6D\x61\x70\x74\x69\x6F\x6E\x00\x30\x00\x01\x83\x45\x4F\x10\x66\x66\x69\x63\x84\x45\x4F\x00\x66\x51\x80\x00\x69\x00\x63\x82\x45\x9E\x80\x11\x94\x03\x80\x01\x81\x45\x32\x44\x46\x38\x44\x30\x00\x34\x43\x2D\x35\x42\x46\x41\x2D\x00\x31\x30\x31\x42\x2D\x42\x44\x45\x52\x35\x80\x45\x41\x41\x80\x43\x34\x80\x05\x32\x03\x88\x45\x80\x98\x67\x72\x61\x6D\x20\x46\x00\x69\x6C\x65\x73\x5C\x43\x6F\x6D\x08\x6D\x6F\x6E\x04\x06\x4D\x69\x63\x72\x00\x6F\x73\x6F\x66\x74\x20\x53\x68\x00\x61\x72\x65\x64\x5C\x4F\x46\x46\x00\x49\x43\x45\x31\x36\x5C\x4D\x53\xC0\x4F\x2E\x44\x4C\x4C\x23\x87\x10\x83\x4D\x00\x20\x31\x36\x2E\x30\x20\x4F\x62\x01\x81\xC1\x20\x4C\x69\x62\x72\x61\x72\x16\x79\x00\x4B\x00\x01\x0F\x82\xD4\x03\x00\x13\x11\x82\x03\xF3\x08\x19\x82\xA8\x54\x68\x69\x00\x73\x57\x6F\x72\x6B\x62\x6F\x6F\x50\x6B\x47\x00\x18\x80\x13\x54\x80\xAB\x69\x10\x00\x73\x00\x57\xC0\x59\x72\x00\x6B\x54\x00\x62\xC0\x01\x6F\xC0\x01\x1A\xCE\x0B\x32\x45\xDA\x0B\x1C\xC0\x12\x00\x00\x48\x42\x01\x31\xB5\x42\x78\x33\x80\x93\x1E\x42\x02\x01\x05\x2C\xC2\x21\xA8\x1C\xB8\x22\x42\x08\x2B\x42\x01\x19\x42\x7C\x80\x53\x68\x65\x65\x74\x31\x47\xC2\x1B\x0A\x53\x40\x23\x65\x40\x58\x74\x00\x31\x00\x9A\x1A\x48\x07\x32\x4E\x07\xE3\x1B\x9A\x9B\xCB\x1B\x02\x07\xC0\x1D\x4D\x6F\x64\x75\x6C\x65\x8D\x00\x1C\x0E\x01\x03\x80\x3B\x64\x00\x75\x82\x98\xB3\x81\x1C\x08\x08\x32\x00\x0F\x08\x4F\x1D\x83\x00\xC4\x91\x4D\x39\x41\xB2\x21\x80\x16\x00\x00\x43\x39\x02\x10\xC2\x02')
    comp = Decompressor()
    comp.setCompressedHeader(chunk[:2])
    del chunk[:2]
    result = comp.decompress(chunk)
    expected = ''
    assert result == expected

