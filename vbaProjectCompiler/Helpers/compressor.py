import struct
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
                foo = self.data[self.decompressed_current]
                bar = self.compressed_container[self.compressed_current]
                self.compressed_container[self.compressed_current] = foo
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
