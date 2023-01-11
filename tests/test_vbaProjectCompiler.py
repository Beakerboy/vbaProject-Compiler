# test_vbaProjectCompiler.py

import pytest
from vbaProjectCompiler.main import *

def test_getFirstDirectoryChainSector():
    assert getFirstDirectoryChainSector() == 1;
