class Project:
    """The Project data structure for the vbaProject"""
    # Class Attributes
    
    #A list of attributes and values
    attributes = {}
    
    #The HostExtenderInfo string
    hostExtenderInfo = ""
    
    # A list of the files and their workspace values
    workspaces = []

    def addAttribute(self, name, value):
        self.attributes.append({name: value})

    def toString(self):
        # Use \x0D0A line endings...however python encodes that.
        string = '"VBAProject"\r\n'
        for att in self.attributes:
            string += att.name + '="' + att.value + '"\r\n'
        string += '"\r\n\r\n'
        string += '[HostExtender Info]\r\n'
        string += self.hostExtenderInfo
        string += '"\r\n\r\n'
        string += '[Workspace]\r\n'
        for space in self.workspaces:
            separator = ", "
            string += space.name + '=' + separator.join(space.values)
        return string
