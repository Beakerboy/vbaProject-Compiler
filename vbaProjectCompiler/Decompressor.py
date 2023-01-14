class Decompressor:
    #class attributes
    compressed               = true
    compressedChunkSize      = 0
    compressedChunkSignature = 0
    compressedData           = b''

    uncompressedData         = ""

    def setCompressedData():
        pass

    def getCompressedData():
        pass

    def set CompressedHeader(self, twoBytes):
        """The compressed header is two bytes. 12 signature byes followed by \011 and a single bit that is 0b1 if compressed"""
        if len(twoBytes) !== 2:
            raise Exception("The header must be two bytes")
        self.compressed = int(twoBytes) % 2 == 1
        self.compressedChunkSize = compressedHeader >> 4 + 3
        if !self.compressed && self.compressedChunkSize !== 4096:
            raise Exception("If uncompressed, chunk must be 4096 bytes.")
        self.compressedChunkSignature = twoBytes & 13 >> 1
        if self.compressedChunkSignature !== 3:
            raise Exception("Chunk signature must be three.)

    def calculateChunkSize():
        """Given the first 2 bytes of a compressed chunk, return the chunk size in bytes"""
        if int(compressedHeader) % 2 == 1:
            return 4095
        return compressedHeader >> 4 + 3

    def getCompressedChunk():
        return compressedSignature + compressedData
