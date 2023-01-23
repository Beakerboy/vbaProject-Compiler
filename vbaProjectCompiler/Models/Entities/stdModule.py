from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class StdModule:

    def __init__(ModuleRecord, name):
        self.type = "Module"
        self.docTlibVer = 0
        super(StdModule, self).__init__(name)
