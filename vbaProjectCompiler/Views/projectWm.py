class ProjectWM:
    """
    The ProjectWM data view for the vbaProject
    """
    def __init__(self, project):
        self.project = project

    def toBytes(self):
        output = b''
        for module in self.project.modules:
            output += module.modName.value + b'\x00' + module.modName.value + b'\x00\x00'
        output += b'\x00\x00\x00\x00'
