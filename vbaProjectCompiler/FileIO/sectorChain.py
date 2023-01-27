import os

class SectorChain:

    def __init__(self):
        # The number of bytes in each sector
        self._sectorSize = 0

        # The chain.
        # Each entry points to the address of the next element in the chain.
        self.chain = []

    def getSectorSize(self):
        return self._sectorSize

    def extendChain():
        pass
