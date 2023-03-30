import struct


class IdSizeField():
    """
    Many Records have the same format, a two bye ID, a four byte size and an
    int value formatted to the defined size.
    """

    def __init__(self, id, size: int, value) -> None:
        self._id = id
        self._size = size
        self._value = value

    def pack(self, codepage_name: str, endien: str) -> bytes:
        endienSymbol = '<' if endien == 'little' else '>'
        format = endienSymbol + "HI"
        if isinstance(self.value, str):
            self.stringValue = self._value
            self._value = bytes(self._value, encoding="ascii")
            format += str(self._size) + "s"
        elif isinstance(self._value, bytes):
            format += str(self._size) + "s"
        elif self._size == 2:
            format += "H"
        elif self._size == 4:
            format += "I"
        else:
            msg = "Received data of type " + type(self._value).__name__
            raise Exception(msg)
        return struct.pack(format, self._id, self._size, self._value)
