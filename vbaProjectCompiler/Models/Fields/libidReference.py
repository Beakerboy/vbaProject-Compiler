class LibidReference():
    def __init__(self, pathType, libidGuid, version,
                 libidLcid, libidPath, libidRegName):
        self.libidReferenceKind = "G" if pathType == "windows" else "H"
        self.libidGuid = libidGuid
        self.version = version
        self.libidLcid = libidLcid
        self.libidPath = libidPath
        self.libidRegName = libidRegName

    def __str__(self):
        return "*\\" + \
            self.libidReferenceKind + \
            + "{" + upper(str(self.libidGuid)) + "}#" + \
            self.version + "#" + \
            self.libidLcid + "#" + \
            self.libidPath + "#" + \
            self.libidRegName

    def __len__(self):
        return len(str(self))
