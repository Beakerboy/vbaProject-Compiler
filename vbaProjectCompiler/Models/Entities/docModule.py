from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class DocModule(ModuleRecord):

    def __init__(self, name):
        self.type = "Document"
        self.docTlibVer = 0
        super(DocModule, self).__init__(name)

    def toProjectModuleString(self):
        return "Document=" + self.modName.value + "/&H" + struct.pack("<I", self.docTlibVer)
