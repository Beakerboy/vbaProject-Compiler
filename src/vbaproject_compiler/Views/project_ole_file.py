from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Views.dirStream import DirStream
# from vbaproject_compiler.Views.project_view import ProjectView
from vbaproject_compiler.Views.project import Project
from vbaproject_compiler.Views.projectWm import ProjectWm
from typing import TypeVar


T = TypeVar('T', bound='ProjectOleFile')


class ProjectOleFile:

    def __init__(self: T, project: VbaProject) -> None:
        self._project = project

    def _create_binary_files(self: T) -> None:
        for module in self._project.get_modules():
            module.write_file()
        dir = DirStream(self._project)
        dir.write_file()
        project = Project(self._project)
        project.write_file()
        project_wm = ProjectWm(self._project)
        project_wm.write_file()
        # views = ("_VBA_PROJECT", "dir", "project_wm", "Project")
        # Create views and write

    def _build_ole_directory(self: T) -> None:
        # directory = StorageDirectory()
        # directory.set_name("VBA")
        for module in self._project.get_modules():
            # path = module.get_name() + '.bin'
            # dir = StreamDirectory()
            # dir.set_name(module.get_name())
            # dir.add_stream(path)
            # directory.add_directory(dir)
            pass
        # return directory

    def _write_ole_file(self: T, dir: str) -> None:
        # ole_file = OleFile()
        # ole_file.add_directory(dir)
        # ole_file.build_file()
        # ole_file.write_file("vbaProject.bin")
        pass

    def write_file(self: T) -> None:
        self._create_binary_files()
        directory = self._build_ole_directory()
        self._write_ole_file(directory)
