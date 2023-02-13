import os
import struct
from vbaProjectCompiler.Directories.rootDirectory import RootDirectory
from vbaProjectCompiler.FileIO.fatChain import FatChain
from vbaProjectCompiler.FileIO.miniChain import MiniChain
from vbaProjectCompiler.Models.Entities.Streams.directoryStream import (
    DirectoryStream
)


class OleFile:

    # class default constructor
    def __init__(self, project):
        self.HEADER_BYTES = 512
        self.project = project

        # Instance Attributes
        self.uMinorVersion = 62
        self.uDllVersion = 3
        self.uSectorShift = 9
        self.uMiniSectorShift = 6
        self.firstDirectoryListSector = 1
        self.firstMiniChainSector = 2
        self.ulMiniSectorCutoff = 4096

        # the FAT chain holds large files, the minifat chain, the minifat data,
        # and the directory tree.
        self._fatChain = FatChain(2 ** self.uSectorShift)

        # The list of pointers to the address of the next file piece
        self._minifatChain = MiniChain(2 ** self.uMiniSectorShift)

        # A list of directories
        self.directory = RootDirectory()

    def getFirstDirectoryListSector(self):
        return self.firstDirectoryListSector

    def setFirstDirectoryListSector(self, i):
        # need to ensure sector is not already reserved
        self.firstDirectoryListSector = i

    def getFirstMiniChainSector(self):
        return self.firstMiniChainSector

    def header(self):
        """Create a 512 byte header sector for a OLE object."""
        packSymbol = '<' if self.project.endien == 'little' else '>'
        LONG_LONG_ZERO = b'\x00\x00\x00\x00\x00\x00\x00\x00'

        absig = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

        format = packSymbol + "8s16s6H10I"
        header = struct.pack(
            format,
            absig,
            LONG_LONG_ZERO + LONG_LONG_ZERO,  # clsid
            self.uMinorVersion,
            self.uDllVersion,
            65534,   # BOM
            self.uSectorShift,
            self.uMiniSectorShift,
            0,    # usReserved
            0,    # ulReserved1
            0,    # csectDir
            self._fatChain.count_fat_chain_sectors(),
            self.firstDirectoryListSector,
            0,    # signature
            self.ulMiniSectorCutoff,
            self.getFirstMiniChainSector(),
            max([len(self._minifatChain.getSectors()), 1]),
            self.getDifStartSector(),
            self.countDifSectors()
        )

        sectFat = self.writeHeaderFatSectorList()
        header += sectFat
        return header

    def getDifStartSector(self):
        """
        The Fat sector lost in the header can only list the position of 109
        sectors.If more sectors are needed, the DIF sector lists these sector
        numbers.
        """
        if len(self.getFatSectors()) <= 109:
            return 0xfffffffe
        # research how Dif works
        return 0

    def countDifSectors(self):
        """
        How many sectors of 512 entries are needed to list the positions of the
        remaining FAT sectors.
        What if sectors are not 512 bytes?
        """
        count = self._fatChain.count_fat_chain_sectors()
        if count <= 109:
            return 0
        return (count - 109 - 1) // (2 ** (self.uSectorShift - 2)) + 1

    def writeHeaderFatSectorList(self):
        """
        Create a 436 byte stream of the first 109 FAT sectors, padded with
        \\xFF.
        """
        packSymbol = '<' if self.project.endien == 'little' else '>'
        # if the list is longer then 109 entries, need to mange the extended
        # MSAT sectors.
        output = b''
        list = self.getFatSectors()
        for sector in list[0:109]:
            output += struct.pack(packSymbol + "I", sector)
        output = output.ljust(436, b'\xff')
        return output

    def getFatSectors(self):
        """
        List which sectors contain FAT chain information. They should be on
        128 sector intervals.
        """
        sectorList = []
        numberOfSectors = (len(self._fatChain) - 1) // 128 + 1
        for i in range(numberOfSectors):
            sectorList.append(i * (2 ** (self.uSectorShift - 2)))
        return sectorList

    def build_file(self):
        """
        Build the OLE file data structures from the project data.
        """
        # packSymbol = '<' if self.project.endien == 'little' else '>'

        directoryStream = DirectoryStream()
        directoryStream.setStorageChain(self._fatChain)
        self._fatChain.addStream(directoryStream)

        self._minifatChain.setStorageChain(self._fatChain)
        self._fatChain.addStream(self._minifatChain)

        # pull data from self.project
        for module in self.project.modules:
            self.directory.addModule(module)
        # add _VBA_Project
        # add dir
        # add projectWm
        # add project
        # Flatten directory tree
        self.streams = self.directory.flatten()
        for stream in self.streams:
            directoryStream.append(stream)
            if stream.type == 2:
                if stream.fileSize() > self.ulMiniSectorCutoff:
                    self._fatChain.addStream(stream)
                else:
                    self._minifatChain.addStream(stream)

    def write_file(self, path):
        """
        Write the OLE file to disk
        """
        f = open(path + '/vbaProject.bin', 'wb+')
        f.write(self.header())
        # extend file to full size
        sectors = len(self._fatChain)
        f.write(b'\x00' * sectors * self._fatChain.getSectorSize())
        
        self._fatChain.write_chain("./fatChain.bin")
        # write directory sectors
        # write minifat chain
        # write minifat data

        # write minifat chain sectors
        f.close()

    def writeFile(self, path):
        """
        Build and Write the OLE file
        """
        self.build_file()
        self.write_file(path)
