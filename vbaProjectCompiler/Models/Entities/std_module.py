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

    def create_cache(self) -> bytes:
        cache = ModuleCache()
        cache.cookie = self.cookie.value
        cache.misc = [0x0316, 0x0222, 0x027D, 3, 0, 2, 0xFFFF, "FFFFFFFF", 0]
        cache.indirect_table = bytes.fromhex("FF FF FF FF 78 00 00 00")

        self._cache = cache.to_bytes()
