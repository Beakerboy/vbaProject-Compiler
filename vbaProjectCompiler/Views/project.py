class Project:
    """
    The Project data view for the vbaProject
    """
    def __init__(self, project):
        self.project = project
        # Attributes
    
        #A list of attributes and values
        self.attributes = {}
    
        #The HostExtenderInfo string
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
            result += bytearray(module.toProjectModuleString(), codePageName) + eol
        result += b'Name="VBAProject"' + eol
        for key in self.attributes:
            result += bytearray(key, codePageName) + b'="' + bytearray(self.attributes[key], codePageName) + b'"' + eol
        result += b'CMG="' + bytearray(self.project.getProtectionState(), codePageName) + b'"' + eol
        result += b'DPB="' + bytearray(self.project.getPassword(), codePageName) + b'"' + eol
        result += b'GC="' + bytearray(self.project.getVisibility(), codePageName) + b'"' + eol
        result += eol
        result += b'[Host Extender Info]' + eol
        result += bytearray(self.hostExtenderInfo, codePageName)
        result += eol + eol
        result += b'[Workspace]' + eol
        for module in modules:
            separator = ", "
            result += bytearray(module.modName.value, codePageName) + b'=' + bytearray(separator.join(map(str, module.workspace)), codePageName)
            result += eol
        return result
