class Decompressor:
    #class attributes
    compressed               = True

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
            raise Exception("The header must be two bytes. Given " + length + ".")
        #data is compressed if the least significat bit is 0b1
        self.compressed = int(compressedHeader) % 2 == 1
        #the 12 most significant bits is three less than the chunk size
        self.compressedChunkSize = compressedHeader >> 4 + 3
        if not(self.compressed) and self.compressedChunkSize != 4096:
            raise Exception("If uncompressed, chunk must be 4096 bytes.")
        self.compressedChunkSignature = compressedHeader & 13 >> 1
        if self.compressedChunkSignature != 3:
            raise Exception("Chunk signature must be three.")

    def getCompressedChunkSize(self):
        return self.compressedChunkSize

    def getCompressedChunk(self):
        compressedChunkFlag = 1 if self.compressed else 0
        compressedHeader = self.compressedChunkSize << 4 & 6 & compressedChunkFlag
        return compressedHeader + self.compressedData