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
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x0F33
    f.seek(offset)
    sig = f.read(1)
    assert sig == b'\x01'
    header = f.read(2)
    comp = Decompressor()
    comp.setCompressedHeader(header)
    assert comp.compressedChunkSize == 171
    readChunk = bytearray(f.read(comp.compressedChunkSize - 2))
    result = comp.decompress(readChunk)
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
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x1EC0
    f.seek(offset)
    sig = f.read(1)
    assert sig == b'\x01'
    header = f.read(2)
    comp = Decompressor()
    comp.setCompressedHeader(header)
    readChunk = bytearray(f.read(comp.compressedChunkSize - 2))
    decompressed = bytearray(comp.decompress(readChunk), encoding="charmap")
    count = 0
    output = ''
    while len(decompressed) > 0:
        output += format(count, 'X') + '   '
        #get 16 Bytes
        stringified = ''
        for i in range(min(16, len(decompressed))):
            char = decompressed.pop(0)
            output += format(char, 'X') + ' '
            stringified += chr(char)
        output += ' ' + stringified + '\n'
        count += 16

    assert output == ''
   
