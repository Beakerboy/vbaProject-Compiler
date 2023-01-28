import os

class SectorChain:

    def __init__(self, size):
        # The number of bytes in each sector
        self._sectorSize = size

        # The chain.
        # Each entry points to the address of the next element in the chain.
        self._chain = []

    def __len__(self):
        return len(self._chain)

    def getSectorSize(self):
        return self._sectorSize

    def getLength(self):
        return len(self._chain)

    def getChain(self):
        return self._chain
