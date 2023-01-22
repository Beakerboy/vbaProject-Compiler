from vbaProjectCompiler.Models.Fields.doubleEncodedString import DoubleEncodedString
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField

class ModuleRecord():
    def __init__(self, codePageName, name, streamName, docString, offset, helpContext, type, readonly=False, private=False):
        self.codePageName = codePageName
        self.modName      = DoubleEncodedString(codePageName, [0x0019, 0x0047], name)
        self.streamName   = DoubleEncodedString(codePageName, [0x001A, 0x0032], streamName)
        self.docString    = DoubleEncodedString(codePageName, [0x001C, 0x0048], docString)
        self.offsetRec    = IdSizeField(0x0031, 4, offset)
        self.helpContext  = IdSizeField(0x001E, 4, helpContext)
        self.cookie       = IdSizeField(0x002C, 2, 0xFFFF)
        self.type         = PackedData("HI", type, 0)
        #self.readonly = SimpleRecord(0x001E, 4, helpContext)
        #self.private = SimpleRecord(0x001E, 4, helpContext)
       
    def pack(self):
        output = self.modName.pack() + self.streamName.pack() + self.docString.pack() + self.offsetRec.pack() + self.helpContext.pack() + self.cookie.pack() + self.type.pack()
        footer = PackedData("HI", 0x002B, 0)
        output += footer.pack()
        return output
