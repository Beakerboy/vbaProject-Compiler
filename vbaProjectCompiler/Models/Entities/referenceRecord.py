from vbaProjectCompiler.Models.Fields.libidReference import LibidReference

class ReferenceRecord():
     def __init__(self, codePageName, name, libidRef):
         self.codePageName = codePageName
         self.RefName = DoubleEncodedSimple(codePageName, [0x0016, 0x003E], name)
         self.libidRef = libidRef

     def pack(self):
         strlen = len(self.libidRef)
         format = "HII" + str(strlen) + "sIH"
         refRegistered = PackedRecord(format, 0x000D, strlen + 10, strlen, str(self.libidRef).encode(self.codePageName), 0, 0)

         return self.RefName.pack() + refRegistered.pack()
