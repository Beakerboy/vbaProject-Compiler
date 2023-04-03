import struct
from typing import TypeVar


T = TypeVar('T', bound='PackedData')


class PackedData():
    """
    Mutivalue field with a packing format
    """
    def __init__(self:T, format: str, *values) -> None:
        self.values = values
        self.format = format

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        endien_symbol = '<' if endien == 'little' else '>'
        return struct.pack(endien_symbol + self.format, *self.values)
