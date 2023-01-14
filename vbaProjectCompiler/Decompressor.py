class Decompressor:
    #class attributes
    compressed = true
    def init():
        pass

    def setCompressedData():
        pass

    def getCompressedData():
        pass

    def set CompressedHeader(self, twoBytes):
        """The compressed header is two bytes. 12 signature byes followed by \011 and a single bit that is 0b1 if compressed"""
        #if len(twoBytes) > 2:
            #throw exception
        self.compressed = int(twoBytes) % 2 == 1
        self.compressedChunkSize = compressedHeader >> 4 + 3
        #if !self.compressed && self.compressedChunkSize !== 4096:
            #throw exception. If uncompressed, chunk must be 4096 bytes.
        self.compressedChunkSignature = twoBytes & 13 >> 1
        if self.compressedChunkSignature !== 3:
            #throw exception. Chunk sig must be three.

    def calculateChunkSize():
        """Given the first 2 bytes of a compressed chunk, return the chunk size in bytes"""
        if int(compressedHeader) % 2 == 1:
            return 4095
        return compressedHeader >> 4 + 3

    def getCompressedChunk():
        return 
