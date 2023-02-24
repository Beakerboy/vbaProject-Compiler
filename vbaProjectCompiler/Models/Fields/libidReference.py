from pathlig import Path
class LibidReference():
    def __init__(self, libidGuid, version,
                 libidLcid, libidPath, libidRegName):
        self.libidGuid = libidGuid
        self.version = version
        self.libidLcid = libidLcid
        self.libidPath = Path(libidPath)
        self.libidRegName = libidRegName
        if type(self.libidPath) == "WindowsPath" or type(self.libidPath) == "PureWindowsPath":
            self.libidReferenceKind = "G"
        else:
            self.libidReferenceKind = "H"

    def __str__(self):
        return "*\\" + \
            self.libidReferenceKind + \
            "{" + str(self.libidGuid).upper() + "}#" + \
            self.version + "#" + \
            self.libidLcid + "#" + \
            self.libidPath + "#" + \
            self.libidRegName

    def __len__(self):
        return len(str(self))
