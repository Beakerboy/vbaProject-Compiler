from vbaProjectCompiler.FileIO.sectorChain import SectorChain


class FatChain(SectorChain):

    def __init__(self, size):
        super().__init__(size)
        self._nextFreeSector = 1

    def getChain(self):
        """ 0x80 should be replaced in case sector is longer
        """
        chain = super().getChain()
        if len(chain) == 0:
            chain = [0xFFFFFFFD]
        else:
            num = (len(self) - 1) // 0x80 + 1
            for i in range(num):
                chain[i * 0x80] = 0xFFFFFFFD
        return chain

    def _reserveNextFreeSector(self):
        if self._nextFreeSector % 0x80 == 0:
            self._nextFreeSector += 1
        sector = self._nextFreeSector
        self._nextFreeSector += 1
        return sector
