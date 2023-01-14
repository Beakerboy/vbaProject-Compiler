class Decompressor:
    #class attributes
    #is the data compressed?
    compressed               = 1

    #the size in bytes of the chunk after compression
    compressedChunkSize      = 0

    #the chunk signature must be 3
    compressedChunkSignature = 3

    #The chunk after compression
    compressedData           = b''

    uncompressedData         = ""

    def setCompressedData():
        pass

    def getCompressedData(self):
        return self.compressedData

    def setCompression(self, compress):
        """Set if we want to compress the source or include it raw"""
        self.compressed = compress

    def setCompressedHeader(self, compressedHeader):
        """The compressed header is two bytes. 12 signature byes followed by \011 and a single bit that is 0b1 if compressed"""
        length = len(compressedHeader)
        if length != 2:
            raise Exception("The header must be two bytes. Given " + str(length) + ".")
        intHeader = int.from_bytes(compressedHeader, "little")
        #data is compressed if the least significat bit is 0b1
        self.compressed = (intHeader & 0x8000) >> 15

        #the 12 most significant bits is three less than the chunk size
        self.compressedChunkSize = (intHeader & 0x0FFF) + 3
        if not(self.compressed) and self.compressedChunkSize != 4096:
            raise Exception("If uncompressed, chunk must be 4096 bytes.")
        self.compressedChunkSignature = (int.from_bytes(compressedHeader, "big") & 14) >> 1
        if self.compressedChunkSignature != 3:
            raise Exception("Chunk signature must be three. Value is " + str(self.compressedChunkSignature) + ".")

    def getCompressedChunkSize(self):
        return self.compressedChunkSize

    def getCompressedChunk(self):
        compressedChunkFlag = 1 if self.compressed else 0
        compressedHeader = self.compressedChunkSize << 4 & 6 & compressedChunkFlag
        return compressedHeader + self.compressedData
