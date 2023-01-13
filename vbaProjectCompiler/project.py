class Project:
    """The Project data structure for the vbaProject"""
    # Class Attributes
    
    #A list of attributes and values
    attributes = {}
    
    #The HostExtenderInfo string
    hostExtenderInfo = ""
    
    # A list of the files and their workspace values
    workspaces = {}

    def addAttribute(self, name, value):
        self.attributes[name] = value

    def addWorkspace(self, name, val1, val2, val3, val4, val5):
        self.workspaces[name] = [val1, val2, val3, val4, val5]

    def toBytearray(self):
        # Use \x0D0A line endings...however python encodes that.
        eol = b'\x0D\0A'
        result = b'"VBAProject"' + eol
        for key in self.attributes:
            result += bytearray(key, 'ascii') + b'="' + bytearray(self.attributes[key], 'ascii') + eol
        result += eol + eol
        result += b'[HostExtender Info]' + eol
        result += bytearray(self.hostExtenderInfo)
        result += eol + eol
        result += b'[Workspace]' + eol
        for key in self.workspaces:
            separator = ", "
            result += bytearray(key, 'ascii') + b'=' + bytearray(separator.join(map(str, self.workspaces[key])), 'ascii')
            result += eol
        #remove last '\r\n'
        return result[:-1]
