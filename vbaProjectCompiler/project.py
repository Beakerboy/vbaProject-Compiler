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

    def toString(self):
        # Use \x0D0A line endings...however python encodes that.
        string = '"VBAProject"\r\n'
        for key in self.attributes:
            string += key + '="' + self.attributes[key] + '"\r\n'
        string += '\r\n\r\n'
        string += '[HostExtender Info]\r\n'
        string += self.hostExtenderInfo
        string += '"\r\n\r\n'
        string += '[Workspace]\r\n'
        for key in self.workspaces:
            separator = ", "
            string += key + '=' + separator.join(map(str, self.workspaces[key]))
            string += "\r\n"
        #remove last '\r\n'
        return string
