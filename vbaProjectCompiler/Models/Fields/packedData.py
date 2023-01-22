import struct
class PackedData():
    """
    Mutivalue field with a packing format
    """
    def __init__(self, format, *values):
        self.values  = values
        self.format = format

    def pack(self):
        return struct.pack("<" + self.format, *self.values)
