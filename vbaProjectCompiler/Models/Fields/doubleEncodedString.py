from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField


class DoubleEncodedString():
    """
    Encode text data twice with different ids and lengths
    """
    def __init__(self, ids: list, text: str) -> None:
        self.ids = ids
        self.value = text

    def pack(self, codepage_name, endien):
        encoded = self.value.encode(codepage_name)
        self.mod_name1 = IdSizeField(self.ids[0], len(encoded), encoded)
        format = "utf_16_le" if endien == 'little' else "utf_16_be"
        encoded = self.value.encode(format)
        self.mod_name2 = IdSizeField(self.ids[1], len(encoded), encoded)
        return (self.mod_name1.pack(codepage_name, endien)
                + self.mod_name2.pack(codepage_name, endien))
