# test_fatChain.py

import pytest
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.FileIO.fatChain import FatChain
from vbaProjectCompiler.Directories.directory import Directory

def test_defaults():
    project = VbaProject()
    chain = FatChain(512)
    assert chain.getLength() == 1
    assert chain.getChain() == [0xfffffffd]
