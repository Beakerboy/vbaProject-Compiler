class LibidReference():
    def __init__(self, libid_guid, version,
                 libid_lcid, libid_path, libid_reg_name):
        self._libid_guid = libid_guid
        self._version = version
        self._libid_lcid = libid_lcid
        self._libid_path = libid_path
        self._libid_reg_name = libid_reg_name
        if self._is_windows_path(libid_path):
            self._libid_reference_kind = "G"
        else:
            self._libid_reference_kind = "H"

    def __str__(self):
        return "*\\" + \
            self._libid_reference_kind + \
            "{" + str(self._libid_guid).upper() + "}#" + \
            self._version + "#" + \
            self._libid_lcid + "#" + \
            str(self._libid_path) + "#" + \
            self._libid_reg_name

    def __len__(self):
        return len(str(self))

    def _is_windows_path(self, path):
        return path[0] != '/'
