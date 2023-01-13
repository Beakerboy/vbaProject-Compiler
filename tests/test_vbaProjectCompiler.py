# test_vbaProject.py

import pytest, binascii, sys
from vbaProjectCompiler.vbaProject import VbaProject

def test_getFirstDirectoryListSector():
    project = VbaProject()
    assert project.getFirstDirectoryListSector() == 1
    project.setFirstDirectoryListSector(2)
    assert project.getFirstDirectoryListSector() == 2

def test_header():
    project = VbaProject()
    result = project.header()
    expected = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3E\x00\x03\x00\xFE\xFF\x09\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\xFE\xFF\xFF\xFF\x00\x00\x00\x00'
    empty = b'\xff\xff\xff\xff'
    emptyLine = empty * 4
    padding = emptyLine * 27
    expected += b'\x00\x00\x00\x00' + padding
    assert result == expected
