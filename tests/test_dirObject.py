# test_vbaProjectCompiler.py
import pytest

from vbaProjectCompiler.decompressor import Decompressor
from vbaProjectCompiler.Directories.dirStream import DirStream

def test_dirStream():
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x1EC0
    f.seek(offset)
    sig = f.read(1)
    header = f.read(2)
    comp = Decompressor()
    comp.setCompressedHeader(header)
    readChunk = bytearray(f.read(comp.compressedChunkSize - 2))
    decompressedStream = comp.decompress(readChunk)
    stream = DirStream()
    result = stream.toBytes()
    expected = decompressedStream[:0x0110]
    assert expected == result
