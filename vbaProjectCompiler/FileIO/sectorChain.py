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
        chain = []
        for stream in self._streams:
            sectors = stream.getSectors()
            max = sectors[-1]
            if max >= len(chain):
                number = max - len(chain)
                chain.extend([0] * number)
            for i in range(len(sectors)):
                sectornum = sectors[i]
                if sectors[i] == max:
                    chain[sectornum] = 0xFFFFFFFE
                else:
                    chain[sectornum] = sectors[i + 1]
                
        return chain


    def reserveNextFreeSector(self):
        sector = self._nextFreeSector
        self._nextFreeSector +=1


    def extendChain(self, stream, number):
        """
        """
        sectorList = []
        for i in range(number):
            sectorList.append(self.reserveNextFreeSector())
        stream.setAdditionalSectors(sectorList)


    def requestNewSectors(self, stream):
        """
        the size of the stream has changed, based on the new size, are additional sectors needed?
        """
        
        pass


    def addStream(self, stream):
        sector = self.startNewChain()
        stream.setStartSector(sector)
        sectorsNeeded = (stream.getSize() - 1) // self._sectorSize + 1
        additionalSectors = self.extendChain(stream, sectorsNeeded)
        stream.setAdditionalSectors(additionalSectors)
        self._streams.append(stream)
