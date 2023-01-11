# test_vbaProjectCompiler.py

import pytest, binascii
from vbaProjectCompiler.main import *

def test_constructor():
    expected = "./Fo0"
    project = VbaProject(expected)
    result = project.path
    assert result == expected

def test_getFirstDirectoryChainSector():
    project = VbaProject('.')
    assert project.getFirstDirectoryChainSector() == 1;

def test_header():
    project = VbaProject('.')
    result = project.header()
    expected = b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3E\x00\x03\x00\xFE\xFF\x09\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\xFE\xFF\xFF\xFF\x00\x00\x00\x00'
    assert result == expected

def test_streamSectors():
    project = VbaProject('.')
    list1 = [7]
    list2 = [4, 5, 6, 8, 16, 9, 10, 11, 12, 13, 14, 15, 17]
    project.addStreamSectorList(list1)
    assert project.countStreams() == 1
    project.addStreamSectorList(list2)
    assert project.countStreams() == 2
    result = project.streamSectors
    assert result == [list1, list2]
    assert project.getFatChainLength() == 1
