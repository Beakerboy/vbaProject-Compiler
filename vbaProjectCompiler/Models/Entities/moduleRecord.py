from vbaProjectCompiler.Models.Fields.doubleEncodedString import DoubleEncodedString
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField

class ModuleRecord():
    def __init__(self, name, docString, helpContext, type, readonly=False, private=False):
        self.modName      = DoubleEncodedString([0x0019, 0x0047], name)
        self.streamName   = DoubleEncodedString([0x001A, 0x0032], name)
        self.docString    = DoubleEncodedString([0x001C, 0x0048], docString)
        self.helpContext  = IdSizeField(0x001E, 4, helpContext)
        self.cookie       = IdSizeField(0x002C, 2, 0xFFFF)
        self.type         = PackedData("HI", type, 0)
        #self.readonly = SimpleRecord(0x001E, 4, helpContext)
        #self.private = SimpleRecord(0x001E, 4, helpContext)

    def addPerformanceCache(self, cache):
        self.cache = cache

    def addWorkspace(self, name, val1, val2, val3, val4, val5):
        self.workspace  = [val1, val2, val3, val4, val5]

    def pack(self, codePageName, endien):
        self.offsetRec = IdSizeField(0x0031, 4, len(self.cache))
        output = self.modName.pack(codePageName, endien) + self.streamName.pack(codePageName, endien) + self.docString.pack(codePageName, endien) + self.offsetRec.pack(codePageName, endien) + self.helpContext.pack(codePageName, endien) + self.cookie.pack(codePageName, endien) + self.type.pack(codePageName, endien)
        footer = PackedData("HI", 0x002B, 0)
        output += footer.pack(codePageName, endien)
        return output
