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
        if intHeader > (2*0x7fff) or 0 > intHeader:
            raise Exception('intHeader out of range: ' + str(intHeader))
        return struct.pack("<H", intHeader)

    def compressRaw(self, input):
        self.compressedChunkSize = 4098
        self.compressedData = input.ljust(4096, '\0')

    def compressStandard(self, input):
        pass

    def decompress(self, data):
        while len(data) > 0:
          #flag is one byte
          flagToken = data.pop(0)
          if len(data) == 0:
              raise Exception("There must be at least one token in each TokenSequence.")
          flagMask = 1
          for i in range(8):
              flag = flagToken & flagMask
              flagMask = flagMask << 1
              if flag == 0:
                  if len(data) > 0:
                      self.uncompressedData += chr(data.pop(0))
              else:
                  if len(data) < 2:
                      raise Exception("Copy Token does not exist. FlagToken was " + str(flagToken) + " and decompressed chunk is " + self.uncompressedData + '.')
                  copyToken = struct.unpack("<H", data[:2])
        return self.uncompressedData

    def copytokenHelp(self):
        """
        Calculate a lengthMask, offsetMask, and bitCount
        """
        difference = len(self.uncompressedData)
        bitCount = self.ceilLog2(difference)
        lengthMask = 0xFFFF >> bitCount
        offsetMask = ~lengthMask
        maxLength = 0xFFFF << bitCount + 3
        return {
            "lengthMask": lengthMask,
            "offsetMask": offsetMask,
            "bitCount": bitCount
        }

    def unpackCopytoken(self, copyToken):
        """
        calculate an offset and length from a copytoken
        """
        help = self.copytokenHelp()
        length = copyToken & help.lengthMask + 3
        temp1 = copyToken & help.offsetMask
        temp2 = 16 - help.bitCount
        offset = temp1 >> temp2 + 1
        return {
            "length": length,
            "offset": offset
        }

    def ceilLog2(self, int):
        """
        calculate the log2 of the integer, rounded up to the nearest integer
        """
        orig_int = int
        if int == 0:
            raise Exception("zero not allowed")
        i = 0
        int = int >> 1
        while int != 0:
            i += 1
            int = int >> 1
        if 2**i < orig_int:
            i += 1
        return i
