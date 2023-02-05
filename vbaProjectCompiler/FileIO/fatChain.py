import os
from vbaProjectCompiler.FileIO.sectorChain import SectorChain


class FatChain(SectorChain):

    def __init__(self, size):
        super().__init__(size)
        self._nextFreeSector = 1


    def getChain(self):
        chain = super(FatChain, self).getChain()
        if len(chain) == 0:
            chain = [0xFFFFFFFD]
        else:
            pass
        return chain


    def reserveNextFreeSector(self):
        sector = self._nextFreeSector
        self._nextFreeSector +=1
        if self._nextFreeSector % 0x80 ==0:
            self._nextFreeSector +=1
