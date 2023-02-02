import struct
class Decompressor:
    #class attributes

    endien                   = ''
    #is the data compressed?
    compressed               = 1

    #the size in bytes of the chunk after compression
    compressedChunkSize      = 0

    #The chunk after compression
    compressedData           = bytearray(b'')

    def __init__(self, endien = 'little'):
        self.endien = endien
        self.uncompressedData = bytearray(b'')

    def setCompressedData(self, data):
        """set the Compressed data attribute"""
        if len(data) != self.compressedChunkSize - 2:
            raise Exception("Expecting " + str(self.compressedChunkSize - 2) + " bytes, but given " + str(len(data)) + ".")
        self.compressedData = data

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

    def getCompressedChunkHeader(self):
        compressedChunkFlag = 1 if self.compressed else 0
        intHeader = (self.compressed << 15) | 0x3000 | (self.compressedChunkSize - 3)
        if intHeader > (2*0x7fff) or 0 > intHeader:
            raise Exception('intHeader out of range: ' + str(intHeader))
        return struct.pack("<H", intHeader)

    def decompress(self, data):
        orig_data = data
        """
        Decompress a bytearray

        :param data bytes: bytes of compressed data
        :return: bytes
        :rtype: bytes
        """
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
                      self.uncompressedData.append(data.pop(0))
              else:
                  if len(data) < 2:
                      raise Exception("Copy Token does not exist. FlagToken was " + str(flagToken) + " and decompressed chunk is " + self.uncompressedData + '.')
                  copyToken = self.unpackCopytoken(struct.unpack("<H", data[:2])[0])
                  del data[:2]
                  
                  for i in range(copyToken["length"]):
                      offset = copyToken["offset"]
                      length = len(self.uncompressedData)
                      self.uncompressedData.append(self.uncompressedData[-1 * offset])
        return self.uncompressedData

    def copytokenHelp(self):
        """
        Calculate a lengthMask, offsetMask, and bitCount
        """
        difference = len(self.uncompressedData)
        bitCount = self.ceilLog2(difference)
        lengthMask = 0xFFFF >> bitCount
        offsetMask = ~lengthMask & 0xFFFF
        maxLength = 0xFFFF << bitCount + 3
        return {
            "lengthMask": lengthMask,
            "offsetMask": offsetMask,
            "bitCount": bitCount
        }

    def unpackCopytoken(self, copyToken):
        """
        calculate an offset and length from a 16 bit copytoken
        """
        help = self.copytokenHelp()
        length = (copyToken & help["lengthMask"]) + 3
        temp1 = copyToken & help["offsetMask"]
        temp2 = 16 - help["bitCount"]
        offset = (temp1 >> temp2) + 1
        return {
            "length": length,
            "offset": offset
        }

    def ceilLog2(self, int):
        i = 4
        while 2 ** i < int:
            i += 1
        return i

class Compressor:
    def __init__(self, data, compress=True):
        self.data = data
	
        # If compress is FALSE, the result will be raw.
        self._compress = compress
        
    def compress(self):
        self.compressed_container = bytearray()
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

    def compress_decompressed_chunk(self):
        self.compressed_container.extend(bytearray(4096 + 2))
        compressed_end = self.compressed_chunk_start + 4098
        self.compressed_current = self.compressed_chunk_start + 2
        decompressed_end = self.decompressed_buffer_end

        if (self.decompressed_chunk_start + 4096) < self.decompressed_buffer_end:
            decompressed_end = (self.decompressed_chunk_start + 4096)

        while (self.decompressed_current < decompressed_end) and (self.compressed_current < compressed_end):
            self.compress_token_sequence(compressed_end, decompressed_end)

        if self.decompressed_current < decompressed_end:
            self.compress_raw_chunk(decompressed_end - 1)
            compressed_flag = 0
        else:
            compressed_flag = 1

        size = self.compressed_current - self.compressed_chunk_start
        header = 0x0000

        # Pack compressed chunk size
        temp1 = header & 0xF000
        temp2 = size - 3
        header = temp1 | temp2

	# Pack compressed chunk flag
        temp1 = header & 0x7FFF
        temp2 = compressed_flag << 15
        header = temp1 | temp2

        # Pack compressed chunk signature
        temp1 = header & 0x8FFF
        header_final = temp1 | 0x3000

        struct.pack_into("<H", self.compressed_container, self.compressed_chunk_start, header_final)

        if (self.compressed_current):
            self.compressed_container = self.compressed_container[0:self.compressed_current]

    def compress_token_sequence(self, compressed_end, decompressed_end):
        flag_byte_index = self.compressed_current
        token_flags = 0
        self.compressed_current = self.compressed_current + 1

        for index in range(0, 8):
            if ((self.decompressed_current < decompressed_end) and (self.compressed_current < compressed_end)):
                token_flags = self.compress_token(compressed_end, decompressed_end, index, token_flags)
        self.compressed_container[flag_byte_index] = token_flags

    def compress_token(self, compressed_end, decompressed_end, index, flags):
        offset = 0
        offset, length = self.matching(decompressed_end)

        if offset:
            if (self.compressed_current + 1) < compressed_end:
                copy_token = self.pack_copy_token(offset, length)
                struct.pack_into("<H", self.compressed_container, self.compressed_current, copy_token)

                # Set flag bit
                temp1 = 1 << index
                temp2 = flags & ~temp1
                flags = temp2 | temp1

                self.compressed_current = self.compressed_current + 2
                self.decompressed_current = self.decompressed_current + length
            else:
                self.compressed_current = compressed_end
        else:
            if self.compressed_current < compressed_end:
                if not(isinstance(self.compressed_current, int)) or not(isinstance(self.decompressed_current, int)):
                    raise Exception("values must be integers compressed_current is " + str(self.compressed_current) + " and decomprssed_current is " + str(self.compressed_current) + ".")
			
                self.compressed_container[self.compressed_current] = self.data[self.decompressed_current]
                self.compressed_current = self.compressed_current + 1
                self.decompressed_current = self.decompressed_current + 1
            else:
                self.compressed_current = compressed_end

        return flags

    def matching(self, decompressed_end):
        candidate = self.decompressed_current - 1
        best_length = 0

        while candidate >= self.decompressed_chunk_start:
            C = candidate
            D = self.decompressed_current
            L = 0
            while D < decompressed_end and (self.data[D] == self.data[C]):
                L = L + 1
                C = C + 1
                D = D + 1

            if L > best_length:
                best_length = L
                best_candidate = candidate
            candidate = candidate - 1

        if best_length >=  3:
            length_mask, off_set_mask, bit_count, maximum_length = self.copy_token_help()
            length = best_length
            if (maximum_length < best_length):
                length = maximum_length
            offset = self.decompressed_current - best_candidate
        else:
            length = 0
            offset = 0

        return offset, length

    def copy_token_help(self):
        difference = self.decompressed_current - self.decompressed_chunk_start
        bit_count = 0

        while ((1 << bit_count) < difference):
            bit_count +=1

        if bit_count < 4:
            bit_count = 4;

        length_mask = 0xFFFF >> bit_count
        off_set_mask = ~length_mask
        maximum_length = (0xFFFF >> bit_count) + 3

        return length_mask, off_set_mask, bit_count, maximum_length

    def pack_copy_token(self, offset, length):
        length_mask, off_set_mask, bit_count, maximum_length = self.copy_token_help()
        temp1 = offset - 1
        temp2 = 16 - bit_count
        temp3 = length - 3
        copy_token = (temp1 << temp2) | temp3

        return copy_token

    def compress_raw_chunk(self):
        self.compressed_current = self.compressed_chunk_start + 2
        self.decompressed_current  = self.decompressed_chunk_start
        pad_count = 4096
        last_byte = self.decompressed_chunk_start + pad_count
        if self.decompressed_buffer_end < last_byte:
            last_byte =  self.decompressed_buffer_end

        for index in range(self.decompressed_chunk_start, last_byte):
            self.compressed_container[self.compressed_current] = self.data[index]
            self.compressed_current = self.compressed_current + 1
            self.decompressed_current = self.decompressed_current + 1
            pad_count = pad_count - 1

        for index in range(0, pad_count):
            self.compressed_container[self.compressed_current] = 0x0;
            self.compressed_current = self.compressed_current + 1
