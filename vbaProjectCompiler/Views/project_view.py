import struct


class ProjectView:
    """
    The _VBA_PROJECT data view for the vbaProject
    """
    def __init__(self, project) -> None:
        self.project = project

    def to_bytes(self) -> bytes:
        endienSymbol = '<' if self.project.endien == 'little' else '>'
        format = endienSymbol + "HHBH"
        output = b''
        reserved1 = 0x61CC
        reserved2 = 0x00
        reserved3 = 0x0003
        cache_version = self.project.get_performance_cache_version()

        output += struct.pack(format, reserved1, cache_version,
                              reserved2, reserved3)
        return output + self.project.get_performance_cache()

    def write_file(self) -> None:
        bin_f = open("vba_project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
