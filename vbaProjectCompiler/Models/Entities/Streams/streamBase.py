
class StreamBase:
    """
    Base class for any object which will appear as a stream within a sector chain
    """

    def __init__(self):

        # The stuff that will be used to squeeze data into the chain.
        # It can just be the data itself.
        self._data = b''

        # An array of sectors this stream will reside
        self._sectors = []

        # An object of type SectorChain which will be storing this stream
        self._storageChain = 0


    def setStorageChain(self, chain):
        self._storageChain = chain


    def setStartSector(self, sector):
        """
        Set the location of the first sector of the file
        Must be run first
        """
        self._sectors = [sector]


    def getStartSector(self):
        return self._sectors[0]


    def setAdditionalSectors(self, sectors):
        self._sectors.extend(sectors)


    def getSectors(self):
        return self._sectors


    def append(self, data):
        """
        Extend the data in this stream. Request additional chain storage if needed
        """
        self._extendData(data)
        currentSecCnt = len(self._sectors)
        self._storageChain.requestNewSectors(self)


    def streamSize(self):
        """
        The size the stream will be when rendered
        """
        return len(self._data)


    def to_bytes():
        """
        Return the object in bytes form
        """
        pass


    def _extendData(self, data):
        """
        Add new data to the bytearray
        """
        self._data += data

