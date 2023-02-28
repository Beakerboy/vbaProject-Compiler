from vbaProjectCompiler.Models.Entities.module_base import ModuleBase
from vbaProjectCompiler.Models.Entities.module_cache import ModuleCache


class StdModule(ModuleBase):

    def __init__(self, name):
        super(StdModule, self).__init__(name)
        self.type = "Module"

    def normalize_file(self):
        f = open(self._file_path, "r")
        new_f = open(self._file_path + ".new", "a+", newline='\r\n')
        while line := f.readline():
            new_f.writelines([line])
        new_f.close()
