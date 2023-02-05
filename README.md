[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/vbaProject-Compiler/badge.svg?branch=main)](https://coveralls.io/github/Beakerboy/vbaProject-Compiler?branch=main)
# vbaProject-Compiler
Create a vbaProject.bin file from VBA source files.


## VBAProject Class

The vbaProject class contains all the data and metadata that will be used to create the OLE container.


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

