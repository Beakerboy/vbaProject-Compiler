import binascii
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

    def to_bytes(self):
        project = self.project
        codePageName = project.getCodePageName()
        # Use \x0D0A line endings...however python encodes that.
        eol = b'\x0D\x0A'
        project_id = project.getProjectId()
        id = bytearray(project_id, codePageName)
        result = b'ID="' + id + b'"' + eol
        modules = project.modules
        for module in modules:
            result += bytes(module.toProjectModuleString(), codePageName) + eol
        result += b'Name="VBAProject"' + eol
        for key in self.attributes:
            result += self._attr(key, self.attributes[key])
        cmg = ms_ovba_crypto.encrypt(
                                     project_id,
                                     project.get_protection_state()
                                    )
        dpb = ms_ovba_crypto.encrypt(project_id, project.get_password())
        gc = ms_ovba_crypto.encrypt(project_id, project.get_visibility_state())
        result += (bytes('CMG="', codePageName)
                   + binascii.hexlify(cmg).upper()
                   + b'\x22\x0D\x0A')
        result += (bytes('DPB="', codePageName)
                   + binascii.hexlify(dpb).upper()
                   + b'\x22\x0D\x0A')
        result += (bytes('GC="', codePageName)
                   + binascii.hexlify(gc).upper()
                   + b'\x22\x0D\x0A')
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
