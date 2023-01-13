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
        result = b'"VBAProject" + eol
        for key in self.attributes:
            string += bytearray(key) + b'="' + bytearray(self.attributes[key]) + eol
        string += eol + eol
        string += b'[HostExtender Info]' + eol
        string += bytearray(self.hostExtenderInfo)
        string += eol + eol
        string += b'[Workspace]' + eol
        for key in self.workspaces:
            separator = ", "
            string += bytearray(key) + b'=' + bytearray(separator.join(map(str, self.workspaces[key])))
            string += eol
        #remove last '\r\n'
        return string
