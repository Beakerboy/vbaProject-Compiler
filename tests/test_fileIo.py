# test_vbaProject.py

import pytest, binascii, sys
from os.path import exists
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.oleFile import OleFile

def test_getFirstDirectoryListSector():
    vbaProject = VbaProject()
    project = OleFile(vbaProject)
    assert project.getFirstDirectoryListSector() == 1
    project.setFirstDirectoryListSector(2)
    assert project.getFirstDirectoryListSector() == 2

def test_header():
    vbaProject = VbaProject()
    project = OleFile(vbaProject)
    result = project.header()
    expected = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3E\x00\x03\x00\xFE\xFF\x09\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\xFE\xFF\xFF\xFF\x00\x00\x00\x00'
    empty = b'\xff\xff\xff\xff'
    emptyLine = empty * 4
    padding = emptyLine * 27
    expected += b'\x00\x00\x00\x00' + padding
    assert result == expected

def test_write():
    vbaProject = VbaProject()
    project = OleFile(vbaProject)
    project.write(".")
    assert exists('./vbaProject.bin')
