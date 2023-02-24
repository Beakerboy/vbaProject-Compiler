class LibidReference():
    def __init__(self, libidGuid, version,
                 libidLcid, libidPath, libidRegName):
        self.libidGuid = libidGuid
        self.version = version
        self.libidLcid = libidLcid
        self.libidPath = libidPath
        self.libidRegName = libidRegName
        path_type = type(self.libidPath)
        if self._is_windows_path(libidPath):
            self.libidReferenceKind = "G"
        else:
            self.libidReferenceKind = "H"

    def __str__(self):
        return "*\\" + \
            self.libidReferenceKind + \
            "{" + str(self.libidGuid).upper() + "}#" + \
            self.version + "#" + \
            self.libidLcid + "#" + \
            str(self.libidPath) + "#" + \
            self.libidRegName

    def __len__(self):
        return len(str(self))

    def _is_windows_path(self, path):
        return path[0] != '/'
