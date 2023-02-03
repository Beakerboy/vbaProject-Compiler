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
        self.compressed_current = 0
        self.compressed_chunk_start = 0
        self.decompressed_current = 0
        self.decompressed_buffer_end = len(self.data)
        self.decompressed_chunk_start = 0
	
        signature_byte = 0x01
        self.compressed_container.append(signature_byte)
        self.compressed_current = self.compressed_current + 1
        while self.decompressed_current < self.decompressed_buffer_end:
            self.compressed_chunk_start = self.compressed_current
            self.decompressed_chunk_start = self.decompressed_current
            self.compress_decompressed_chunk()

        return self.compressed_container

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
            uncompressesData, compressedTokenSequence = self.compressTokenSequence(uncompressedData)
            chunk += compressedTokenSequence

        chunkSize = len(chunk)
        # if the compression algorithm produces a chunk too large, use raw.
        if chunkSize > 4096:
            chuckSize = 4096
            chunk = data.ljust(4096, '\0')
            compressAndSig = 0x3000
        header = compressAndSig & chunkSize
        packSymbol = '<' if self.endian == 'little' else '>'
        format = packSymbol + 'H'
        chunk = struct.pack(format, header) + chunk
        return chunk

    def compressTokenSequence(self, data):
        uncompressedData = data
        tokenFlag = b'\x00'
        tokens = b''
        for i in range(8):
            if len(uncompressedData) > 0:
                token = b''
                tokenflag = 0
                uncompressedData, token, flag = self.compressToken(uncompressedData)
                tokenFlag = (flag << i) | tokenFlag
                tokens += token
        tokenSequence = tokenFlag + tokens
        return uncompressedData, tokenSequence

    def compressToken(self, uncompressedData):
        """
        Given a sequence of uncompressed data, return a single compressed token. Tokens are either:
        one byte representing the value of the token
        two bytes indicating the location and length of the replacement sequence
        the flag byte is 1 if replacement took place
        """
        offset, length = self.matching(uncompressedData)
        if length == 0:
            uncompressedData = uncompressedData[1:]
        else:
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
            D = candidate + 1
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
            maximumLength = self.copytokenHelp(uncompressedStream)
            length = min(maximumLength, bestLength)
            offset = len(self.activeChunk) - len(uncompressedStream) - bestCandidate
        return offset, length

    def copytokenHelp(self, uncompressedStream):
        """
        Calculate a lengthMask, offsetMask, and bitCount
        """
        difference = len(self.uncompressedChunk) - len(uncompressedStream)
        bitCount = self.ceilLog2(difference)
        lengthMask = 0xFFFF >> bitCount
        offsetMask = ~lengthMask & 0xFFFF
        maxLength = 0xFFFF << bitCount + 3
        return maxLength
        
    def ceilLog2(self, int):
        i = 4
        while 2 ** i < int:
            i += 1
        return i
