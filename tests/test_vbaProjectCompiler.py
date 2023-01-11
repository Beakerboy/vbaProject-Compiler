# test_vbaProjectCompiler.py

import pytest
from vbaProjectCompiler.main import *

def test_formatLittleEndien():
    assert formatLittleEndien(1, 4) == "01000000";
