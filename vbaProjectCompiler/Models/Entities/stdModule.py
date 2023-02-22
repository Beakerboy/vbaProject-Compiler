from vbaProjectCompiler.Models.Entities.moduleRecord import ModuleRecord


class StdModule(ModuleRecord):

    def __init__(self, name):
        super(StdModule, self).__init__(name)
        self.type = "Module"

    def create_cache(self):
        ca = create_cache_header(cookie, b'\x22', b'\x88\c01', b'\x29',
                                 b'\x7D\x02', b'\x03\x00', b'\x02', b'\x00')
        data2 = b'\xFF\xFF\xFF\xFF\x78\x00\x00\x00'
        ca = (ca + create_cache_middle(b'', b'', data2)
              + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              + create_cache_footer(b'\xFF'))
        return ca
