class ProjectWm:
    """
    The ProjectWM data view for the vbaProject
    """
    def __init__(self, project):
        self.project = project

    def toBytes(self):
        output = b''
        for module in self.project.modules:
            output += bytearray(module.modName.value, 'ascii') + b'\x00' + bytearray(module.modName.value, 'utf_16_le') + b'\x00\x00'
        output += b'\x00\x00'
        return output
