# test_fileIO.py
from os.path import exists
from vbaProjectCompiler.vbaProject import VbaProject

def test_fileCreation():
    project = VbaProject()
    filePath = './vbaProject.bin'
    project.writeFile(filePath)
    assert exists(filePath)
