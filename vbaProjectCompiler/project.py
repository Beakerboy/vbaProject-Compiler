class Project:
    """The Project data structure for the vbaProject"""
    # Class Attributes
    
    #A list of attributes and values
    attributes = []
    hostExtenderInfo = ""
    
    # A list of the files and their workspace values
    workspaces = []
    
    toString(self):
      #\x0D0A line endings
        string = "\"VBAProject"\r\n"
        for att in attributes:
            string += att.name + '="' + att.value . '"\r\n'
        string += '"\r\n\r\n'
        string += '[HostExtender Info]\r\n'
        string += self.hostExtenderInfo
        string += '"\r\n\r\n'
        string += '[Workspace]\r\n'
        for space in workspaces:
            string += space.name + '=' + join(space.values, ', ')
        return string
