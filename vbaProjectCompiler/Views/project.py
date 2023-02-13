import ms_ovba_crypto


class Project:
    """
    The Project data view for the vbaProject
    """
    def __init__(self, project):
        self.project = project
        # Attributes

        # A list of attributes and values
        self.attributes = {}

        # The HostExtenderInfo string
        self.hostExtenderInfo = ""

    def addAttribute(self, name, value):
        self.attributes[name] = value

    def toBytearray(self):
        codePageName = self.project.getCodePageName()
        # Use \x0D0A line endings...however python encodes that.
        eol = b'\x0D\x0A'

        id = bytearray(self.project.getProjectId(), codePageName)
        result = b'ID="' + id + b'"' + eol
        modules = self.project.modules
        for module in modules:
            result += bytes(module.toProjectModuleString(), codePageName) + eol
        result += b'Name="VBAProject"' + eol
        for key in self.attributes:
            result += self._attr(key, self.attributes[key])
        cmg = ms_ovba_crypto.encrypt(self.project.getProtectionState())
        dpb = ms_ovba_crypto.encrypt(self.project.getPassword())
        gc = ms_ovba_crypto.encrypt(self.project.getVisibilityState())
        result += self._attr("CMG", cmg)
        result += self._attr("DPB", dpb)
        result += self._attr("GC", gc)
        result += eol
        result += b'[Host Extender Info]' + eol
        result += bytes(self.hostExtenderInfo, codePageName)
        result += eol + eol
        result += b'[Workspace]' + eol
        for module in modules:
            separator = ", "
            result += bytes(module.modName.value, codePageName) + b'='
            joined = separator.join(map(str, module.workspace))
            result += bytes(joined, codePageName)
            result += eol
        return result

    def _attr(self, name, value):
        codePageName = self.project.getCodePageName()
        eol = b'\x0D\x0A'
        b_name = bytes(name, codePageName)
        b_value = bytes(value, codePageName)
        return b_name + b'="' + b_value + b'"' + eol
