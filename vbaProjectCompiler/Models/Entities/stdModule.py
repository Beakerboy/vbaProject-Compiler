from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class StdModule:

    def __init__(ModuleRecord, name):
        self.type = "Document"
        self.docTlibVer = 0
        super(StdModule, self).__init__(name)

    def toProjectModuleString(self):
        return "Module=" + self.modName.value
