# test_vbaProjectCompiler.py

import pytest
from vbaProjectCompiler.main import *

def test_ getFirstDirectoryChainSector():
    assert getFirstDirectoryChainSector() == 0x01000000;
