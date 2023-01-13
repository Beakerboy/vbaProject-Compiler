# test_vbaProjectCompiler.py

import pytest
from vbaProjectCompiler.main import *

def test_defaults():
    project = VbaProject()
    #Test that only one fat chain sector is needed when no data is present
    assert project.countFatChainSectors == 1

    #Test that by default, the Fat chain will reside in sector zero
    assert project.fatChainSectorList() == [0]

    #Test that when no data is present, all streams are terminated after the first sector
    assert project.fatChain == [-2, -2, -2]
    
