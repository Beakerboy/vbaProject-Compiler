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
    libidRef = LibidReference(
            "windows",
            "{00020430-0000-0000-C000-000000000046}",
            "2.0",
            "0",
            "C:\\Windows\\System32\\stdole2.tlb",
            "OLE Automation"
        )
        oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
        libidRef2 = LibidReference(
            "windows",
            "{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}",
            "2.0",
            "0",
            "C:\\Program Files\\Common Files\\Microsoft Shared\\OFFICE16\\MSO.DLL",
            "Microsoft Office 16.0 Object Library"
        )
        officeReference = ReferenceRecord(codePageName, "Office", libidRef2)
        stream.addReference(oleReference)
        stream.addReference(officeReference)
    expected = bytes(decompressedStream)
    assert stream.toBytes() == expected
