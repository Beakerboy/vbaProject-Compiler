class VBA_Project:
    """
    The _VBA_PROJECT data view for the vbaProject
    """
    def __init__(self, project):
        self.project = project

    def toBytes(self):
        endienSymbol = '<' if self.project.endien == 'little' else '>'
        format = endienSymbol + "HHcH"
        output = b''
        reserved1 = 0x61CC
        reserved2 = 0x00
        reserved3 = 0x0003

        output += struct.pack(format, reserved1, self.project.getPermormanceCacheVersion(), reserved2, reserved3)
        return output + self.project.getPerformanceCache()
