[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/vbaProject-Compiler/badge.svg?branch=main)](https://coveralls.io/github/Beakerboy/vbaProject-Compiler?branch=main)
# vbaProject-Compiler
Create a vbaProject.bin file from VBA source files.


## VBAProject Class

The vbaProject class contains all the data and metadata that will be used to create the OLE container.

```python
from vbaProjectCompiler.vbaProject import VbaProject
from vbaProjectCompiler.ole_file import OleFile


project = VbaProject()
thisWorkbook = DocModule("ThisWorkbook")
thisWorkbook.addFile(path)
project.addModule(thisWorkbook)

ole_file = OleFile(project)
ole_file.writeFile(".")
```

The VbaProject class has many layers of customization available. Forexample a librry referenece can be added to the project.

```python
codePage = 0x04E4
codePageName = "cp" + str(codePage)
libidRef = LibidReference(
    "windows",
    "{00020430-0000-0000-C000-000000000046}",
    "2.0",
    "0",
    "C:\\Windows\\System32\\stdole2.tlb",
    "OLE Automation"
)
oleReference = ReferenceRecord(codePageName, "stdole", libidRef)
project.addReference(oleReference)
```

## oleFile Class

Users should not have to interact with the oleFile class. It's job is to extract the data from the vbaProject and turn it into a valid file. This includes deciding which data stream appears where, and applying different views to the models to save the data in the correct formats.

The oleFIle has two parts, a header and a FAT Sector Chain. This FAT chain stores multiple streams of data:
* Fat Chain Stream
* Directory Stream
* Minifat Chain Stream
* Minifat Data Stream
* Fat Data Stream

These are all different views of data from the following Models

* fatChain
* minifatChain
* directoryStream
