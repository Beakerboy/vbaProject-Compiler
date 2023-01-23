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
        modules = self.project.modules
        codePageName = self.project.getCodePageName()
        # Use \x0D0A line endings...however python encodes that.
        eol = b'\x0D\x0A'
        result = b'"VBAProject"' + eol
        for key in self.attributes:
            result += bytearray(key, 'ascii') + b'="' + bytearray(self.attributes[key], 'ascii') + b'"' + eol
        result += eol
        result += b'[Host Extender Info]' + eol
        result += bytearray(self.hostExtenderInfo, 'ascii')
        result += eol + eol
        result += b'[Workspace]' + eol
        for module in modules:
            separator = ", "
            result += bytearray(module.name, codePageName) + b'=' + bytearray(separator.join(map(str, module.workspace)), codePageName)
            result += eol
        return result
