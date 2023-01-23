from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord

class StdModule(ModuleRecord):

    def __init__(self, name):
        super(StdModule, self).__init__(name)
        self.type = "Module"
