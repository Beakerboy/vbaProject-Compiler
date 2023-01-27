import os

class SectorChain:

    def __init__(self):
        # The number of bytes in each sector
        self._sectorSize = 0

        # The chain.
        # Each entry points to the address of the next element in the chain.
        self._chain = []

    def getSectorSize(self):
        return self._sectorSize

    def extendChain(self, start, length):
        """
        Extend the chain that starts at sector {start} by {length} additional sectors
        """
        pass

    def writeDataToSector(self, file, sector, data = b'\x00'):
        """
        Write the provided data to a specific sector.
        Overwriting the existing data.
        """
        pass
