from vbaProjectCompiler.Models.Entities.Streams.streamBase import StreamBase


class DirectoryStream(StreamBase):
    """
    The directory stream is an arrary of directory records
    """

    def __init__(self):
       self._data = []

    def _extendData(self, data):
       """
       Add new data to the bytearray
       """
       self._data.append(data)
