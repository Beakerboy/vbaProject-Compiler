from vbaProjectCompiler.FileIO.sectorChain import SectorChain
class FatChain(SectorChain):

    def writeDataToSector(self, file, sector, data = b'\x00'):
        dataLength = len(data)
        if dataLength > self._sectorSize:
            raise Exception("Data length is " + str(dataLength) + " bytes. Longer than a sector")
        if dataLength < self._sectorSize:
            data = data.ljust(self._sectorSize, b'\x00')
        # Check File length and fill up to the desired sector
        fileLength = file.seek(-1, os.SEEK_END)
        desiredLength = 512 + sector * self._sectorSize
        if fileLength < desiredLength:
            file.write(b'\x00' * (desiredLength - fileLength))
        file.write(data)
