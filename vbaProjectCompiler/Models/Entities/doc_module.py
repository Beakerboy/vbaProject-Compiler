from ms_ovba_compression.ms_ovba import MsOvba
from vbaProjectCompiler.Models.Entities.module_base import ModuleBase
from vbaProjectCompiler.Models.Entities.module_cache import ModuleCache


class DocModule(ModuleBase):
    """
    A Document Module is a module record that is associated with a worksheet or
    workbook.
    """
    def __init__(self, name):
        self.docTlibVer = 0
        super(DocModule, self).__init__(name)
        self.type = "Document"

        # GUID
        self._guid = ""

    def toProjectModuleString(self):
        return ("Document=" + self.modName.value + "/&H"
                + self.docTlibVer.to_bytes(4, "big").hex())

    def set_guid(self, guid):
        """
        Should probably abstract this to add other attributes to the file
        during normalization.
        """
        self._guid = guid

    def normalize_file(self):
        f = open(self._file_path, "r")
        new_f = open(self._file_path + ".new", "a+", newline='\r\n')
        for i in range(5):
            line = f.readline()

        new_f.write(line)
        txt = self._attr("Base", '"0{' + str(self._guid).upper() + '}"')
        new_f.writelines([txt])
        while line := f.readline():
            new_f.writelines([line])
        new_f.writelines([self._attr("TemplateDerived", "False")])
        new_f.writelines([self._attr("Customizable", "True")])
        new_f.close()
        bin_f = open(self._file_path + ".bin", "wb")
        bin_f.write(self._cache)
        with open(self._file_path + ".new", mode="rb") as new_f:
            contents = new_f.read()
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(contents)
        bin_f.write(compressed)
        bin_f.close()

    def create_cache(self):
        cache = ModuleCache()
        cache.cookie = self.cookie.value
        cache.misc = [0x0316, 0x02D2, 0x032D, 0x0123, 0x88, 8, 0x18,
                      "00000000", 1]
        cache.guid = bytes(("0{" + str(self._guid) + "}").upper(), "utf_16_le")

        indirect_table = ("02 80 FE FF FF FF FF FF 20 00 00 00 FF FF FF FF",
                          "30 00 00 00 02 01 FF FF 00 00 00 00 00 00 00 00",
                          "FF FF FF FF FF FF FF FF 00 00 00 00 2E 00 43 00",
                          "1D 00 00 00 25 00 00 00 FF FF FF FF 40 00 00 00")
        cache.indirect_table = bytes.fromhex(" ".join(indirect_table))
        object_table = ("02 00 53 4C FF FF FF FF 00 00 01 00 53 10 FF FF",
                        "FF FF 00 00 01 00 53 94 FF FF FF FF 00 00 00 00",
                        "02 3C FF FF FF FF 00 00")
        cache.object_table = bytes.fromhex(" ".join(object_table))
        self.cache = cache.to_bytes()
