import os
from vbaProjectCompiler.FileIO.sectorChain import SectorChain
class FatChain(SectorChain):

    def __init__(self, size):
        super(FatChain, self).__init__(size)
        self._chain = [0xfffffffd]

    def writeDataToSector(self, file, sector, data = b'\x00'):
        dataLength = len(data)
        if dataLength > self._sectorSize:
            raise Exception("Data length is " + str(dataLength) + " bytes. Longer than a sector")
        if dataLength < self._sectorSize:
            data = data.ljust(self._sectorSize, b'\x00')
        # Check File length and fill up to the desired sector
        fileLength = file.seek(-1, os.SEEK_END)
        desiredLength = 512 + sector * self._sectorSize
        if fileLength < desiredLength:
            file.write(b'\x00' * (desiredLength - fileLength))
        file.write(data)

    def extendChain(self, start, number):
        """
        The fat chain needs to ensure that new sectors do not land on any sectors which will be
        for fat chain information.
        """
        if number < 1:
            raise Exception("Number must be greater than zero.")
        if start >= len(self._chain):
            raise Exception("Chain does not exist at that address.")
        if self._chain[start] == 0xFFFFFFFD:
            raise Exception("Unable to start on a Fat Chain sector.")
        newSectors = []
        lastSector = start
        nextSector = start
        while nextSector != 0xFFFFFFFE:
            lastSector = nextSector
            nextSector = self._chain[lastSector]
        firstFreeSector = len(self._chain)
        # Check That we are not reserving what should be a FAT sector
        if firstFreeSector % 0x80 == 0:
            self._chain.append(0xFFFFFFFD)
            firstFreeSector += 1
        self._chain[lastSector] = firstFreeSector
        newSectors.append(firstFreeSector)
        for i in range(number - 1):
            firstFreeSector += 1
            if len(self._chain) % 0x80 == 0:
                self._chain.append(0xFFFFFFFD)
                firstFreeSector += 1
            self._chain.append(firstFreeSector)
            newSectors.append(firstFreeSector)
        self._chain.append(0xFFFFFFFE)
        return newSectors

    def startNewChain(self):
        """
        We assume sectors are being filled sequentially.
        Start a new single sector chain and return the address.
        """
        if len(self._chain) % 0x80 == 0:
            self._chain.append(0xFFFFFFFD)
        self._chain.append(0xfffffffe)
        return len(self._chain) - 1

    def findSector(self, startSector, depth):
        """
        Follow the fat chain starting at startSector, for depth {depth} to find the sector.
        depth is zero or greater.
        """
        sector = startSector
        for i in range(depth):
            sector = self._chain[sector]
        return sector
