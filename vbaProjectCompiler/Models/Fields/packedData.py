import struct
class PackedData():
    """
    Mutivalue field with a packing format
    """
    def __init__(self, format, *values):
        self.values  = values
        self.format = format

    def pack(self, codePageName, endien):
        endienSymbol = '<' if endien == 'little' else '>'
        return struct.pack(endienSymbol + self.format, *self.values)
