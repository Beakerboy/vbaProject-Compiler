import os
from vbaProjectCompiler.FileIO.sectorChain import SectorChain
class MiniChain(SectorChain):

    def addStream(self, data):
        sectors = (len(data) - 1) // self._sectorSize + 1
        sectorNumber = len(self._chain)
        newSectors = []
        for i in range(sectors - 1):
            newSectors.append(sectorNumber)
            self._chain.append(sectorNumber + 1)
            sectorNumber += 1
        self._chain.append(0xFFFFFFFE)
        newSectors.append(sectorNumber)
        return newSectors
