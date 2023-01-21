class LibidReference():
    def __init__(self, pathType, libidGuid, version, libidLcid, libidPath, libidRegName):
        self.LibidReferenceKind = "G" if pathType == "windows" else "H"
        self.libidGuid = libidGuid
        self.version = version
        self.libidLcid = libidLcid
        self.libidPath = libidPath
        self.libidRegName = libidRegName

    def toString(self):
        return "*\\" + \
            self.LibidReferenceKind + \
            self.libidGuid + "#" + \
            self.version + "#" + \
            self.libidLcid + "#" + \
            self.libidPath + "#" + \
            self.libidRegName
