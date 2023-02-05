import os
from vbaProjectCompiler.FileIO.sectorChain import SectorChain
from vbaProjectCompiler.Models.Entities.Streams.streamBase import StreamBase


class MiniChain(SectorChain, StreamBase):

    def __init__(self, size):
        super().__init__(size)


    def addStream(self, stream):
        """
        Add a new stream to the minifat chaain and arrange the storage resources
        We need to manage changes to the minifat chain, minifat stream, and the
        FAT resources for them.
        """

        # If we have not started a minifat data stream in the FAT chain
        # start one now.
        if len(self._streams) == 0:
            self._streams = StreamBase()
            self._storageChain.addStream(self._streams)

        # Create a new entry on the minifat chain and tell the stream what it is
        sector = self._startNewChain()
        stream.setStartSector(sector)

        # Figure out how many more are needed and pass it on to the stream
        sectorsNeeded = (stream.streamSize() - 1) // self._sectorSize + 1
        additionalSectors = self.extendChain(sector, sectorsNeeded)
        stream.setAdditionalSectors(additionalSectors)
        self._streams.append(stream)


    def extendChain(self, stream, number):
        """
        """
        sectorList = []
        for i in range(number):
            sectorList.append(self._reserveNextFreeSector())
        stream.setAdditionalSectors(sectorList)


    def _startNewChain(self):
        # Increase the necessary chain resources by one address
        newSector = self._reserveNextFreeSector()
        self.append(1)
        return newSector

 
    def streamSize(self):
        """
        implementation of StreamBase.streamSize()
        """
        return 4 * len(self)


    def _extendData(self, number):
        """
        implementation of StreamBase._extendData()
        """
        pass

