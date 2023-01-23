import struct
from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class DocModule(ModuleRecord):

    def __init__(self, name):
        self.docTlibVer = 0
        super(DocModule, self).__init__(name)
        self.type = "Document"

    def toProjectModuleString(self):
        return "Document=" + self.modName.value + "/&H" + str(struct.pack("<I", self.docTlibVer))
