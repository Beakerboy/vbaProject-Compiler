# from ms_cfb import OleFile
# from ms_cfb.Models.Directories.storage_directory import StorageDirectory
# from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from vbaProjectCompiler.Models.Entities.module_base import ModuleBase
from vbaProjectCompiler.Models.Entities.reference_record import ReferenceRecord
from vbaProjectCompiler.Views.dirStream import DirStream
# from vbaProjectCompiler.Views.project_view import ProjectView
from vbaProjectCompiler.Views.project import Project
from vbaProjectCompiler.Views.projectWm import ProjectWm
from typing import TypeVar


T = TypeVar('T', bound='VbaProject')


class VbaProject:

    def __init__(self: T) -> None:

        self.endien = 'little'

        # Protected Instance Attributes
        self._codepage_name = 'cp1252'
        self._project_id = '{}'
        self._protection_state = b'\x00\x00\x00\x00'
        self._password = b'\x00'
        self._visibility_state = b'\xFF'
        self._performance_cache = b''
        self._performance_cache_version = 0xFFFF

        # A list of directories
        self.directories = []
        self.references = []
        self.modules = []

        self._project_cookie = 0xFFFF

    # Getters and Setters
    def set_project_id(self: T, id: str) -> None:
        self._project_id = id

    def get_project_id(self: T) -> str:
        return self._project_id

    def set_protection_state(self: T, state: int) -> None:
        self._protection_state = state

    def get_protection_state(self: T) -> int:
        return self._protection_state

    def set_visibility_state(self: T, state: int) -> None:
        """
        0   = not visible
        255 = visible
        """
        if state != 0 and state != 255:
            raise Exception("Bad visibility value.")
        self._visibility_state = state

    def get_visibility_state(self: T) -> bytes:
        return self._visibility_state

    def set_password(self: T, value: bytes) -> None:
        self._password = value

    def get_password(self: T) -> bytes:
        return self._password

    def set_performance_cache(self: T, cache: bytes) -> None:
        self._performance_cache = cache

    def get_performance_cache(self: T) -> None:
        return self._performance_cache

    def set_performance_cache_version(self: T, version: int) -> None:
        self._performance_cache_version = version

    def get_performance_cache_version(self: T) -> int:
        return self._performance_cache_version

    def get_codepage_name(self: T) -> str:
        return self._codepage_name

    def set_project_cookie(self: T, value: int) -> None:
        self._project_cookie = value

    def get_project_cookie(self: T) -> int:
        return self._project_cookie

    # Appenders
    def add_module(self: T, mod: ModuleBase) -> None:
        self.modules.append(mod)

    def add_reference(self: T, ref: ReferenceRecord) -> None:
        self.references.append(ref)

    def _create_binary_files(self: T) -> None:
        for module in self.modules:
            module.write_file()
        dir = DirStream(self)
        dir.write_file()
        project = Project(self)
        project.write_file()
        project_wm = ProjectWm(self)
        project_wm.write_file()
        # views = ("_VBA_PROJECT", "dir", "project_wm", "Project")
        # Create views and write

    def _build_ole_directory(self: T) -> None:
        # directory = StorageDirectory()
        # directory.set_name("VBA")
        for module in self.modules:
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
