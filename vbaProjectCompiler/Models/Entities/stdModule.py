from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord


class StdModule(ModuleRecord):

    def __init__(self, name):
        super(StdModule, self).__init__(name)
        self.type = "Module"

    def create_cache(self)->bytes:
        id_table = 0x0188.to_bytes(2, "little")
        ca = self._create_cache_header(self.cookie, b'\x22', id_table,
                                       b'\x7D\x02', b'\x03\x00',
                                       b'\x00', b'\x02', b'\xFF\xFF')
        data2 = b'\xFF\xFF\xFF\xFF\x78\x00\x00\x00'
        ca = (ca + self._create_cache_middle(b'', [], data2)
              + b'\x00\x00'
              + self._create_cache_footer(b'\xFF'))
        magic = (len(ca) - 0x3C).to_bytes(2, "little")
        ca = ca[:0x19] + magic + ca[0x1B:]
        ca += self._create_pcode()
      
        self._cache = ca
