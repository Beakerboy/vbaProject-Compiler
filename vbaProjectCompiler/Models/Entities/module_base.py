from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaProjectCompiler.Models.Fields.packedData import PackedData
from vbaProjectCompiler.Models.Fields.idSizeField import IdSizeField


class ModuleBase():
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
        self._cache = b''
        self.workspace = [0, 0, 0, 0, 'C']
        self.type = ''
        self.created = 0
        self.modified = 0
        self._fileSize = 0
        self._size = 0

    def set_cache(self, cache):
        self._cache = cache

    def get_cache(self):
        return self._cache

    def get_name(self):
        return self.modName.value

    def addWorkspace(self, val1, val2, val3, val4, val5):
        self.workspace = [val1, val2, val3, val4, val5]

    def pack(self, codePageName, endien):
        """
        Pack the metadata for use in the dir stream.
        """
        typeIdValue = 0x0022 if self.type == 'Document' else 0x0021
        typeId = PackedData("HI", typeIdValue, 0)
        self.offsetRec = IdSizeField(0x0031, 4, len(self._cache))
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

    def write_file(self):
        bin_f = open(self._file_path + ".bin", "wb")
        bin_f.write(self._cache)
        with open(self._file_path + ".new", mode="rb") as new_f:
            contents = new_f.read()
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(contents)
        bin_f.write(compressed)
        bin_f.close()

    def _attr(self, name, value):
        return 'Attribute VB_' + name + ' = ' + value + '\n'
