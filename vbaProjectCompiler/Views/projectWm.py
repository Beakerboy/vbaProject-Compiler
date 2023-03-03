class ProjectWm:
    """
    The ProjectWM data view for the vbaProject
    """
    def __init__(self, project):
        self.project = project

    def to_bytes(self):
        output = b''
        for module in self.project.modules:
            output += (bytes(module.modName.value, 'ascii')
                       + b'\x00'
                       + bytes(module.modName.value, 'utf_16_le')
                       + b'\x00\x00')
        output += b'\x00\x00'
        return output

    def write_file(self):
        bin_f = open("project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
