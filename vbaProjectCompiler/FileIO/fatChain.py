import os
from vbaProjectCompiler.FileIO.sectorChain import SectorChain
class FatChain(SectorChain):

    def reserveNextFreeSector(self):
        sector = self._nextFreeSector
        self._nextFreeSector +=1
        if self._nextFreeSector % 0x80 ==0:
            self._nextFreeSector +=1
