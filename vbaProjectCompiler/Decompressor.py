class Decompressor:
    def calculateChunkSize(compressedHeader):
        """Given the first 2 bytes of a compressed chunk, return the chunk size in bytes"""
        if int(compressedHeader) % 2 == 1:
            return 4095
        return compressedHeader >> 4 + 3
