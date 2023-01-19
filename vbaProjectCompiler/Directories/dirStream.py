from vbaProjectCompiler.Directories.streamDirectory import StreamDirectory

class DirStream(StreamDirectory):
    """
    The dir stream is compressed on write
    """

    def __init__(self):
        
        syskind = {"id": 1, "size": 4, "value": 3] #0=16bit, 1=32bit, 2=mac, 3=64bit
        compatVersion = [74, 4, 3]
        lcid = [2, 4, 0x0409]
        lcidInvoke = [12, 4, 0x0409]
        codePage = [3, 2, 0x04E4]
        projectName = [4, 10, "VBAProject"]
        self.information = [
            syskind,
            compatVersion,
            lcid,
            lcidInvoke,
            codePage,
            projectName
        ]
        self.references  = []
        self.modules = []

    def toBytes(self):
        output = b''
        for record in self.information
            format = "<HI"
            if isinstance(record["value"], str):
                format += record["size"] + "s"
            elif record["size"] == 2:
                format += "H"
            el if record["size"] == 4:
                format += "I"
            output += struct.pack(format, record["id"], record["size"])
            if size == 2:
        return output
