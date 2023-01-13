from vbaProjectCompiler.directory import Directory
from vbaProjectCompiler.vbaProject import VbaProject

def main(args):
    rootPath = args[1]
    vbaProject = VbaProject()
    #for each .bas file in rootPath/Modules
    # compress file
    # add file to the project

    #for each .cls file in rootPath/ClassModules
    # compress file
    # add file to the project

    #for each .frm file in rootPath/Forms
    # compress file
    # add file to the project

    #Create the file
    with open(rootPath + '/vbaProject.bin', 'w+') as file:
        file.write(vbaProject.header())
        #iterate along the FAT chain to write the bin
