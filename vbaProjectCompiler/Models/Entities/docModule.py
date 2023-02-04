from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord


class DocModule(ModuleRecord):
    """
    A Document Module is a module record that is associated with a worksheet or
    workbook.
    """
    def __init__(self, name):
        self.docTlibVer = 0
        super(DocModule, self).__init__(name)
        self.type = "Document"

    def toProjectModuleString(self):
        return "Document=" + self.modName.value + "/&H" + self.docTlibVer.to_bytes(4, "big").hex()
