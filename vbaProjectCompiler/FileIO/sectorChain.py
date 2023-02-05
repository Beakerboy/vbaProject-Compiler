import os

class SectorChain:

    def __init__(self, size):
        # The number of bytes in each sector
        self._sectorSize = size

        # The next available sector on the chain
        self._nextFreeSector = 0

        # Each stream begins at the start of a sector and is padded to fill
        # the end of a sector.
        self._streams = []

    def __len__(self):
        return len(self._chain)

    def getSectorSize(self):
        return self._sectorSize

    def getLength(self):
        return len(self._chain)

    def getChain(self):
        return self._chain

    def addStream(self, stream):
        sector = self.startNewChain()
        stream.setStartSector(sector)
        sectorsNeeded = (stream.getSize() - 1) // self._sectorSize + 1
        additionalSectors = self.extendChain(sector, sectorsNeeded)
        stream.setAdditionalSectors(additionalSectors)
        self._streams.append(stream)
