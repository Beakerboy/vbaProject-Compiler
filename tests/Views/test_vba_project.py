from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.Views.project_view import ProjectView


def test_vba_project() -> None:
    vba_project = VbaProject()
    vba_project_view = ProjectView(vba_project)
    expected = b'\xCC\x61\xFF\xFF\x00\x03\x00'
    assert vba_project_view.to_bytes() == expected
    vba_project.set_performance_cache(b'\x00\x01\x02\x03')
    vba_project.set_performance_cache_version(0x00B5)
    expected = b'\xCC\x61\xB5\x00\x00\x03\x00\x00\x01\x02\x03'
    assert vba_project_view.to_bytes() == expected
