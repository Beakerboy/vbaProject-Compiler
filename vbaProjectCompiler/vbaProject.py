# from ms_cfb import OleFile
# from ms_cfb.Models.Directories.storage_directory import StorageDirectory
# from ms_cfb.Models.Directories.stream_directory import StreamDirectory

from vbaProjectCompiler.Views.dirStream import DirStream
# from vbaProjectCompiler.Views.project_view import ProjectView
from vbaProjectCompiler.Views.project import Project
from vbaProjectCompiler.Views.projectWm import ProjectWm


class VbaProject:

    def __init__(self):

        self.endien = 'little'

        # Protected Instance Attributes
        self._codePageName = 'cp1252'
        self._projectId = '{}'
        self._protection_state = b'\x00\x00\x00\x00'
        self._password = b'\x00'
        self._visibility_state = b'\xFF'
        self._performanceCache = b''
        self._performanceCacheVersion = 0xFFFF

        # A list of directories
        self.directories = []
        self.references = []
        self.modules = []

        self.projectCookie = 0xFFFF

    # Getters and Setters
    def setProjectId(self, id):
        self._projectId = id

    def getProjectId(self):
        return self._projectId

    def set_protection_state(self, state):
        self._protection_state = state

    def get_protection_state(self):
        return self._protection_state

    def set_visibility_state(self, state):
        """
        0   = not visible
        255 = visible
        """
        if state != 0 and state != 255:
            raise Exception("Bad visibility value.")
        self._visibility_state = state

    def get_visibility_state(self):
        return self._visibility_state

    def set_password(self, value):
        self._password = value

    def get_password(self):
        return self._password

    def setPerformanceCache(self, cache):
        self._performanceCache = cache

    def getPerformanceCache(self):
        return self._performanceCache

    def setPerformanceCacheVersion(self, version):
        self._performanceCacheVersion = version

    def getPerformanceCacheVersion(self):
        return self._performanceCacheVersion

    def getCodePageName(self):
        return self._codePageName

    def setProjectCookie(self, value):
        self.projectCookie = value

    # Appenders
    def addModule(self, ref):
        self.modules.append(ref)

    def addReference(self, ref):
        self.references.append(ref)

    def _create_binary_files(self):
        for module in self.modules:
            module.write_file()
        dir = DirStream(self)
        dir.write_file()
        project = Project(self)
        project.write_file()
        projectWm = ProjectWm(self)
        projectWm.write_file()
        # views = ("_VBA_PROJECT", "dir", "projectWm", "Project")
        # Create views and write

    def _build_ole_directory(self):
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

    def _write_ole_file(self, dir):
        # ole_file = OleFile()
        # ole_file.add_directory(dir)
        # ole_file.build_file()
        # ole_file.write_file("vbaProject.bin")
        pass

    def write_file(self):
        self._create_binary_files()
        directory = self._build_ole_directory()
        self._write_ole_file(directory)
