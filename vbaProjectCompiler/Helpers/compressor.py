import struct
class Compressor:
    def __init__(self, endian='little'):
        self.endian = endian

        # The compressed container begins with a sgnature byte and an empty header
        self.compressedData = bytearray(b'\x01')

    def compress(self, data):
        """
        Compress a bytearray

        :param data bytes: bytes of compressed data
        :return: compressed data
        :rtype: bytes
        """
	
        self.originalData = data

        numberOfChunks = (len(data) - 1) // 4096 + 1
        
        for i in range(numberOfChunks):
            chunk = self.compressChunk(data[i * 4096: (i + 1) * 4096])
            self.compressedData += chunk
            
        return self.compressedData

    def compressChunk(self, data):
        """
        A chunk of data is 4096 bytes or less. This will return a stream of max length 4098, a 2 byte header and up to 4096 bytes of data.
        """
        self.activeChunk = data
        # Initialize with an empty header
        # Is endian-ness supposed to affect the header organization?
        # The docs state 12 length bits + 0b011 + compression-bit but real world little endian file has compression-bit + 0b011 + 12 length bits
        compressAndSig = 0xB000
        uncompressedData = data
        chunk = b''
        while len(uncompressedData) > 0:
            uncompressedData, compressedTokenSequence = self.compressTokenSequence(uncompressedData)
            chunk += compressedTokenSequence

        chunkSize = len(chunk)
        # if the compression algorithm produces a chunk too large, use raw.
        if chunkSize > 4096:
            chunkSize = 4096
            chunk = data.ljust(4096, '\0')
            compressAndSig = 0x3000
        header = compressAndSig & chunkSize
        packSymbol = '<' if self.endian == 'little' else '>'
        format = packSymbol + 'H'
        chunk = struct.pack(format, header) + chunk
        return chunk

    def compressTokenSequence(self, data):
        uncompressedData = data
        tokenFlag = 0
        tokens = b''
        for i in range(8):
            if len(uncompressedData) > 0:
                token = b''
                uncompressedData, token, flag = self.compressToken(uncompressedData)
                tokenFlag = (flag << i) | tokenFlag
                tokens += token
        tokenSequence = bytes(tokenFlag) + tokens
        return uncompressedData, tokenSequence

    def compressToken(self, uncompressedData):
        """
        Given a sequence of uncompressed data, return a single compressed token. Tokens are either:
        one byte representing the value of the token
        two bytes indicating the location and length of the replacement sequence
        the flag byte is 1 if replacement took place
        """
        token, length = self.matching(uncompressedData)
        if len(token) == 1:
            uncompressedData = uncompressedData[1:]
            tokenFlag = 0
        else:
            tokenFlag = 1
            uncompressedData = uncompressedData[length:]
        return uncompressedData, token, tokenFlag

    def matching(self, uncompressedStream):
        """
        Work backwards through the uncompressed data that has already been compressed to find the longest series of matching bytes
        """
        offset = 0
        length = 0
        bestLength = 0
        bestCandidate = 0
        candidate = len(self.activeChunk) - len(uncompressedStream) - 1
        while candidate >= 0:
            C = candidate
            D = len(self.activeChunk) - len(uncompressedStream)
            L = 0
            while D < len(self.activeChunk) and self.activeChunk[D] == self.activeChunk[C]:
                C += 1
                D += 1
                L += 1
            if L > bestLength:
                bestLength = L
                bestCandidate = candidate
            candidate -= 1
            
        if bestLength >= 3:
            difference =  len(self.activeChunk) - len(uncompressedStream)
            help = self.copytokenHelp(difference)
            maximumLength = help["maxLength"]
            length = min(maximumLength, bestLength)
            offset = len(self.activeChunk) - len(uncompressedStream) - bestCandidate
            copyToken = self.packCopyToken(length, offset, help)
        else:
            copyToken = bytes(uncompressedStream[0])
        return copyToken, length

    def copytokenHelp(self, difference):
        """
        Calculate a lengthMask, offsetMask, and bitCount from the length of the uncompressedData
        """
        bitCount = self.ceilLog2(difference)
        lengthMask = 0xFFFF >> bitCount
        offsetMask = ~lengthMask & 0xFFFF
        maxLength = 0xFFFF << bitCount + 3
        return {
            "lengthMask": lengthMask,
            "offsetMask": offsetMask,
            "bitCount": bitCount,
            "maxLength": maxLength
        }

    def packCopyToken(self, length, offset, help):
        """
        Create the copy token from the length, offset, and currect position
        
        return bytes
        """
        temp1 = offset - 1
        temp2 = 16 - help["bitCount"]
        temp3 = length - 3
        return struct.pack("<H", (temp1 << temp2) | temp3)

    def ceilLog2(self, int):
        i = 4
        while 2 ** i < int:
            i += 1
        return i
