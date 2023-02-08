from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField


class ModuleRecord():
    def __init__(self, name):
        """
        Initialize the module record
        """
        self.modName = DoubleEncodedString([0x0019, 0x0047], name)
        self.streamName = DoubleEncodedString([0x001A, 0x0032], name)
        self.docString = DoubleEncodedString([0x001C, 0x0048], "")
        self.helpContext = IdSizeField(0x001E, 4, 0)
        self.cookie = IdSizeField(0x002C, 2, 0xFFFF)

        # self.readonly = SimpleRecord(0x001E, 4, helpContext)
        # self.private = SimpleRecord(0x001E, 4, helpContext)
        self.cache = b''
        self.workspace = [0, 0, 0, 0, 'C']
        self.type = ''
        self.created = 0
        self.modified = 0
        self._fileSize = 0
        self._size = 0

    def getSize(self):
        """ is this method necessary
        """
        return len(self.cache)

    def addPerformanceCache(self, cache):
        self.cache = cache

    def addWorkspace(self, val1, val2, val3, val4, val5):
        self.workspace = [val1, val2, val3, val4, val5]

    def pack(self, codePageName, endien):
        """
        Pack the metadata for use in the dir stream.
        """
        typeIdValue = 0x0022 if self.type == 'Document' else 0x0021
        typeId = PackedData("HI", typeIdValue, 0)
        self.offsetRec = IdSizeField(0x0031, 4, len(self.cache))
        output = (self.modName.pack(codePageName, endien)
                  + self.streamName.pack(codePageName, endien)
                  + self.docString.pack(codePageName, endien)
                  + self.offsetRec.pack(codePageName, endien)
                  + self.helpContext.pack(codePageName, endien)
                  + self.cookie.pack(codePageName, endien)
                  + typeId.pack(codePageName, endien))
        footer = PackedData("HI", 0x002B, 0)
        output += footer.pack(codePageName, endien)
        return output

    def toProjectModuleString(self):
        return self.type + "=" + self.modName.value

    def add_file(self, file_path):
        self._file_path = file_path

    def getData(self):
        """
        """
        # Read the compresses file
        # Combine it with the performanceCache
        return self.cache

    def getChunkOfData(self, size, number):
        """
        Split the data into chucks of size {size} and
        return the {number}th chunk
        """
        pass

    def normalize_file(self):
        f = open(self._file_path, "r")
        new_f = open(self._file_path + ".new", "a+", newline='\r\n')
        for i in range(5):
            line = f.readline()

        new_f.write(line)
        txt = 'Attribute VB_Base = "0{00020819-0000-0000-C000-000000000046}\n"'
        new_f.writelines([txt])
        while line := f.readline():
            new_f.writelines([line])
        new_f.writelines(['Attribute VB_TemplateDerived = False'])
        new_f.writelines(['Attribute VB_Customizable = True'])
        new_f.close()
