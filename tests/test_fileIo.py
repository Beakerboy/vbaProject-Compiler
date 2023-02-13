import pytest, binascii, sys
from os.path import exists
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.ole_file import OleFile


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
    expe = (b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x3E\x00\x03\x00\xFE\xFF\x09\x00'
          + b'\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
          + b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x02\x00\x00\x00'
          + b'\x01\x00\x00\x00\xFE\xFF\xFF\xFF\x00\x00\x00\x00')
    empty = b'\xff\xff\xff\xff'
    emptyLine = empty * 4
    padding = emptyLine * 27
    expe += b'\x00\x00\x00\x00' + padding
    assert result == expe


def test_write():
    vbaProject = VbaProject()
    project = OleFile(vbaProject)
    project.writeFile(".")
    assert exists('./vbaProject.bin')


def test_minifatSectors():
    vbaProject = VbaProject()
    project = OleFile(vbaProject)
    assert project.findMinifatSectorOffset(0) == 1536
    project.fatChain.append(6)
    project.fatChain.append(6)
    project.fatChain.append(6)
    assert project.findMinifatSectorOffset(11) == 512 * 7 + 64 * 3