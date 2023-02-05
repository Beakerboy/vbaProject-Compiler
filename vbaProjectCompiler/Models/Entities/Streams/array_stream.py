from vbaProjectCompiler.Models.Entities.Streams.streamBase import StreamBase


class ArrayStream(StreamBase):
    """
    Base class for any object which will appear as a stream within a sector chain
    """

    def __init__(self):
        StreamBase.__init__(self)

        # This object stors data in an array
        self._data = []

    def __iter__(self):
        return iter(self._data)

    def _extendData(self, data):
        """
        Add new data to the bytearray
        """
        self._data.append(data)