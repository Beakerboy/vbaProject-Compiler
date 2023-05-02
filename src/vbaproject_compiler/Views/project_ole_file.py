from ms_cfb.ole_file import OleFile
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Views.dirStream import DirStream
from vbaproject_compiler.Views.project_view import ProjectView
from vbaproject_compiler.Views.project import Project
from vbaproject_compiler.Views.projectWm import ProjectWm
from typing import TypeVar


T = TypeVar('T', bound='ProjectOleFile')


class ProjectOleFile:

    def __init__(self: T, project: VbaProject) -> None:
        self._project = project

    def _create_binary_files(self: T) -> None:
        """
        Create all the custom views for the OLE file:
            dir
            project
            projectWm
            vbs_project
        ToDo
            SLP streams
        """
        for module in self._project.get_modules():
            module.write_file()
        dir = DirStream(self._project)
        dir.write_file()
        project = Project(self._project)
        project.write_file()
        project_wm = ProjectWm(self._project)
        project_wm.write_file()
        project_view = ProjectView(self._project)
        project_view.write_file()

    def _build_ole_directory(self: T) -> RootDirectory:
        """
        Organize the modules and views into the correct storage directories
        """
        directory = RootDirectory()
        storage = StorageDirectory("VBA")
        for module in self._project.get_modules():
            dir = StreamDirectory(module.get_name(), module.get_bin_path())
            storage.add_directory(dir)
        directory.add_directory(storage)
        stream = StreamDirectory("PROJECTwm", "projectwm.bin")
        directory.add_directory(stream)
        stream = StreamDirectory("PROJECT", "project.bin")
        directory.add_directory(stream)
        return directory

    def _write_ole_file(self: T, root: str) -> None:
        ole_file = OleFile()
        ole_file.set_root_directory(root)
        ole_file.create_file("vbaProject.bin")

    def write_file(self: T) -> None:
        self._create_binary_files()
        directory = self._build_ole_directory()
        self._write_ole_file(directory)
