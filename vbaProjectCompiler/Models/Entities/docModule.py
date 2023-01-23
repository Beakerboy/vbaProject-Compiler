from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class DocModule:

    def __init__(ModuleRecord, name):
        self.type = "Document"
        self.docTlibVer = 0
        super(DocModule, self).__init__(name)

    toProjectModuleString(self):
        return "Document=" + self.modName.value + "/&H" + struct.pack("<I", self.docTlibVer)
