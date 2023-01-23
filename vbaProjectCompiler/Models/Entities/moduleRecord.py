from vbaProjectCompiler.Models.Fields.doubleEncodedString import DoubleEncodedString
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField

class ModuleRecord():
    def __init__(self, name):
        """
        Initialize the module record
        """
        self.modName      = DoubleEncodedString([0x0019, 0x0047], name)
        self.streamName   = DoubleEncodedString([0x001A, 0x0032], name)
        self.docString    = DoubleEncodedString([0x001C, 0x0048], "")
        self.helpContext  = IdSizeField(0x001E, 4, 0)
        self.cookie       = IdSizeField(0x002C, 2, 0xFFFF)
       
        #self.readonly = SimpleRecord(0x001E, 4, helpContext)
        #self.private = SimpleRecord(0x001E, 4, helpContext)
        self.cache = b''
        self.workspace = [0, 0, 0, 0, 'C']
        self.type = ''
    
    def addPerformanceCache(self, cache):
        self.cache = cache

    def addWorkspace(self, val1, val2, val3, val4, val5):
        self.workspace  = [val1, val2, val3, val4, val5]

    def pack(self, codePageName, endien):
        typeIdValue = 0x0021 if self.type == 'Document' else 0x0022
        typeId = PackedData("HI", type, typeId) 
        self.offsetRec = IdSizeField(0x0031, 4, len(self.cache))
        output = self.modName.pack(codePageName, endien) + self.streamName.pack(codePageName, endien) + self.docString.pack(codePageName, endien) + self.offsetRec.pack(codePageName, endien) + self.helpContext.pack(codePageName, endien) + self.cookie.pack(codePageName, endien) + typeId.pack(codePageName, endien)
        footer = PackedData("HI", 0x002B, 0)
        output += footer.pack(codePageName, endien)
        return output
