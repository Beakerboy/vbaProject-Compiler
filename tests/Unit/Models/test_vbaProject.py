from vbaProjectCompiler.vbaProject import VbaProject


def test_bad_visibility():
    """
    Visibility must be zero or 0xFF
    """
    project = VbaProject()
    with pytest.raises(Exception):
        project.set_visibility_state(1)
