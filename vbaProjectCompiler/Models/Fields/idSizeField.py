import struct


class IdSizeField():
    """
    Many Records have the same format, a two bye ID, a four byte size and an
    int value formatted to the defined size.
    """

    def __init__(self, id, size, value):
        self.id = id
        self.size = size
        self.value = value

    def pack(self, codePageName, endien):
        endienSymbol = '<' if endien == 'little' else '>'
        format = endienSymbol + "HI"
        if isinstance(self.value, str):
            self.stringValue = self.value
            self.value = bytes(self.value, encoding="ascii")
            format += str(self.size) + "s"
        elif isinstance(self.value, bytes):
            format += str(self.size) + "s"
        elif self.size == 2:
            format += "H"
        elif self.size == 4:
            format += "I"
        else:
            msg = "Received data of type " + type(self.value).__name__
            raise Exception(msg)
        return struct.pack(format, self.id, self.size, self.value)
