import pytest
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField


def test_bad_value():
    field = IdSizeField(2, 3, 6)
    with pytest.raises(Exception):
        field.pack(1234, "little")
