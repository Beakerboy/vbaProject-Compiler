import struct


class PackedData():
    """
    Mutivalue field with a packing format
    """
    def __init__(self, format, *values) -> None:
        self.values = values
        self.format = format

    def pack(self, codepage_name, endien) -> bytes:
        endien_symbol = '<' if endien == 'little' else '>'
        return struct.pack(endien_symbol + self.format, *self.values)
