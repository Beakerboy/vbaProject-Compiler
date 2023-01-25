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

    #Test that when no data is present, all streams are terminated after the first sector
    #current library does not include any directory streams, so no data stream is present.
    #If This test starts to fail with [-2, -2, -2] change the test.
    assert oleFile.fatChain == [-2, -2]
    
def test_longerDirectoryList():
    #Test that when we add four files to the directory, the directory list is one longer.
    project = VbaProject()
    olefile = OleFile(project)
    assert oleFile.countDirectoryListSectors() == 1
    olefile.finalize()
    assert oleFile.countDirectoryListSectors() == 2
    #assert project.fatChain == [4, -2, -2, -2]
