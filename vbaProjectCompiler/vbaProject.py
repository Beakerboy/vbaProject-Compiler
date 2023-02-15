from ms_cfb import OleFile
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory

from vbaProjectCompiler.Views.dirStream import DirStream
from vbaProjectCompiler.Views.vba_Project import Vba_Project
from vbaProjectCompiler.Views.project import Project
from vbaProjectCompiler.Views.projectWm import ProjectWm


class VbaProject:

    def __init__(self):

        self.endien = 'little'

        # Protected Instance Attributes
        self._codePageName = 'cp1252'
        self._projectId = '{}'
        self._protectionState = b'\x00\x00\x00\x00'
        self._password = b'\x00'
        self._visibilityState = b'\xFF'
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

    def setProtectionState(self, state):
        self._protectionState = state

    def getProtectionState(self):
        return self._protectionState

    def setVisibilityState(self, state):
        """
        0   = not visible
        255 = visible
        """
        if state != 0 or state != 255:
            raise Exception("Bad visibility value.")
        self._visibilityState = state

    def getVisibilityState(self):
        return self._visibilityState

    def setPassword(self, value):
        self._password = value

    def getPassword(self):
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

    def write_file(self):
        ole_file = OleFile()
        VBADirectory = StorageDirectory()
        VBADirectory.set_name("VBA")
        for module in self.project.modules:
            path = module.get_name() + '.bin'
            f = open(path, "wb")
            f.write(module.to_bytes())
            f.close()
            dir = StreamDirectory()
            dir.set_name(module.get_name())
            dir.add_stream(path)
            VBADirectory.add_directory(dir)
        path = "_VBA_PROJECT.bin"
        view = Vba_Project()
        f = open(path, "wb")
        f.write(view.to_bytes())
        f.close()
        dir = StreamDirectory()
        dir.set_name("_VBA_PROJECT")
        dir.add_stream(path)
        VBADirectory.add_directory(dir)

        path = "dir.bin"
        view = DirStream()
        f = open(path, "wb")
        f.write(view.to_bytes())
        f.close()
        dir = StreamDirectory()
        dir.set_name("dir")
        dir.add_stream(path)
        VBADirectory.add_directory(dir)
        ole_file.add_directory(VBADirectory)

        path = "projectWm.bin"
        view = ProjectWm()
        f = open(path, "wb")
        f.write(view.to_bytes())
        f.close()
        dir = StreamDirectory()
        dir.set_name("Projectwm")
        dir.add_stream(path)
        ole_file.add_directory(dir)

        path = "project.bin"
        view = Project()
        f = open(path, "wb")
        f.write(view.to_bytes())
        f.close()
        dir = StreamDirectory()
        dir.set_name("Project")
        dir.add_stream(path)
        ole_file.add_directory(dir)
        ole_file.build_file()
        ole_file.write_file("vbaProject.bin")
