
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField

class DoubleEncodedText():
    """
    Encode text data twice with different ids and lengths
    """
    def __init__(self, codePageName, ids, text):
        self.codePageName = codePageName
        encoded = text.encode(codePageName)
        self.modName1 = IdSizeField(ids[0], len(encoded), encoded)
        encoded = text.encode("utf_16_le")
        self.modName2 = IdSizeField(ids[1], len(encoded), encoded)

    def pack(self):
        return self.modName1.pack() + self.modName2.pack()
