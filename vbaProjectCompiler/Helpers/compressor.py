import struct
class Compressor:
    def __init__(self, endian='little'):
        self.endian = endian
 
        # The compressed container begins with a sgnature byte and an empty header
        self.compressedData = bytearray(b'\x01')
	
        # If compress is FALSE, the result will be raw.
        self._compress = compress
        
    def compress(self, data):
        """
        Compress a bytearray

        :param data bytes: bytes of compressed data
        :return: compressed data
        :rtype: bytes
        """
	
        self.uncompresssdData = data

        numberOfChunks = (len(data) - 1) // 4096 + 1
        
        for i in range(numberOfChunks):
            chunk = self.compressChunk(data[i * 4066: (i + 1) * 4096])
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
        
        # Initialize with an empty header
        # Is endian-ness supposed to affect the header organization?
        # The docs state 12 length bits + 0b011 + compression-bit but real world little endian file has compression-bit + 0b011 + 12 length bits
        compressAndSig = 0xB000
        uncompressedData = data
        chunk = b''
        while len(uncompressedData) > 0:
            uncompressesData, compressedTokenSequence = compressTokenSequence(uncompressedData)
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
        chunk = struct.pack(format, header) + chuck
        return chunk

    def compressTokenSequence(self, data):
        uncompressedData = data
        tokenFlag = b'\x00'
        tokens = b''
        for i in range(8):
            if len(uncompressedData) > 0:
                uncompressedData, token, flag = compressToken(uncompressedData)
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
        offset, length = matching(uncompressedData)
        if length == 0:
            uncompressedData = uncompressedData[1:]
        else:
            uncompressedData = uncompressedData[length:]
        return uncompressedData, tokenFlag, token

    def matching(self):
        
        return offset, length
