import struct
class Decompressor:
    #class attributes

    endien                   = ''
    #is the data compressed?
    compressed               = 1

    #the size in bytes of the chunk after compression
    compressedChunkSize      = 0

    #The chunk after compression
    compressedData           = b''

    uncompressedData         = ""

    def __init__(self, endien = 'little'):
        self.endien = endien

    def setCompressedData(self, data):
        """set the Compressed data attribute"""
        if len(data) != self.compressedChunkSize - 2:
            raise Exception("Expecting " + str(self.compressedChunkSize - 2) + " bytes, but given " + str(len(data)) + ".")
        self.compressedData = data

    def setCompression(self, compress):
        """Set if we want to compress the source or include it raw"""
        self.compressed = 1 if compress else 0

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
        self.compressedChunkSignature = (intHeader & 0x7000) >> 12
        if self.compressedChunkSignature != 3:
            raise Exception("Chunk signature must be three. Value is " + str(self.compressedChunkSignature) + ".")

    def getCompressedChunkSize(self):
        return self.compressedChunkSize

    def getCompressedChunk(self):
        
        return self.getCompressedChunkHeader() + self.compressedData

    def compress(self, input):
        if len(input) > 4096:
            raise Exception("Input cannot be longer than 4096 bytes.")
        if self.compress:
            self.compressStandard(input)
        else:
            self.compressRaw(input)
        return self.getCompressedChunkHeader() + self.compressedData

    def getCompressedChunkHeader(self):
        compressedChunkFlag = 1 if self.compressed else 0
        intHeader = (self.compressed << 15) | 0x3000 | (self.compressedChunkSize - 3)
        return struct.pack("<H", intHeader)

    def compressRaw(self, input):
        self.compressedChunkSize = 4098
        self.compressedData = input.ljust(4096, '\0')

    def compressStandard(self, input):
        pass
