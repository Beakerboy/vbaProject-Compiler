
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField

class DoubleEncodedString():
    """
    Encode text data twice with different ids and lengths
    """
    def __init__(self, ids, text):
        self.ids = ids
        self.text = text

    def pack(self, codePageName, endien):
        encoded = self.text.encode(codePageName)
        self.modName1 = IdSizeField(self.ids[0], len(encoded), encoded)
        format = "utf_16_le" if endien == 'little' else "utf_16_be"
        encoded = self.text.encode(format)
        self.modName2 = IdSizeField(self.ids[1], len(encoded), encoded)
        return self.modName1.pack(codePageName, endien) + self.modName2.pack(codePageName, endien)
