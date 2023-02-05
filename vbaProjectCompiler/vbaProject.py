class VbaProject:

    def __init__(self):

        self.endien = 'little'

        # Protected Instance Attributes
        self._codePageName = 'cp1252'
        self._projectId = '{}'
        self._protectionState = "0705D8E3D8EDDBF1DBF1DBF1DBF1"
        self._password = "0E0CD1ECDFF4E7F5E7F5E7"
        self._visibilityState = "1517CAF1D6F9D7F9D706"
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
