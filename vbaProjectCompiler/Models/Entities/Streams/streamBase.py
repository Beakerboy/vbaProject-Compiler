
class StreamBase:
   """
   Base class for any object which will appear as a stream within
   a sector chain
   """

   def __init__(self):
       pass

   def setStorageChain(self, chain):
       self._storageChain = chain

   def append(self, data):
       """
       Extend the data in this stream. Request additional chain storage if needed
       """
       # self._data += data
       self._storageChain.requestNewSectors(len(self._additionalSectors) + 1, self.streamSize())
