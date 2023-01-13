# test_fatChain.py

import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.directory import Directory

def test_defaults():
    project = VbaProject()
    #Test that only one fat chain sector is needed when no data is present
    assert project.countFatChainSectors() == 1

    #Test that by default, the Fat chain will reside in sector zero
    assert project.getFatSectors() == [0]

    #Test that when no data is present, all streams are terminated after the first sector
    #current library does not include any directory streams, so no data stream is present.
    #If This test starts to fail with [-2, -2, -2] change the test.
    assert project.fatChain == [-2, -2]
    
def test_longerDirectoryList():
    #Test that when we add four files to the directory, the directory list is one longer.
    project = VbaProject()
    assert project.countDirectoryListSectors() == 1
    project.finalize()
    assert project.countDirectoryListSectors() == 3
    #assert project.fatChain == [4, -2, -2, -2]
