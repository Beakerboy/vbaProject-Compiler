# test_fatChain.py

import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.oleFile import OleFile
from vbaProjectCompiler.Directories.directory import Directory

def test_defaults():
    project = VbaProject()
    oleFile = OleFile(project)
    #Test that only one fat chain sector is needed when no data is present
    assert oleFile.countFatChainSectors() == 1

    #Test that by default, the Fat chain will reside in sector zero
    assert oleFile.getFatSectors() == [0]

    #Test that when no data is present, all sectors are free.
    assert oleFile.fatChain == [0xfffffffd]
