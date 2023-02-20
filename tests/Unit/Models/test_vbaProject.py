import pytest
from vbaProjectCompiler.vbaProject import VbaProject


test_set_get_visibility():
    project = VbaProject()
    project.set_visibility_state(0)
    assert project.get_visibility_state() == 0

def test_bad_visibility():
    """
    Visibility must be zero or 0xFF
    """
    project = VbaProject()
    with pytest.raises(Exception):
        project.set_visibility_state(1)
