import argparse
import glob
import os
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Models.Entities.doc_module import DocModule
from vbaproject_compiler.Models.Entities.std_module import StdModule
from vbaproject_compiler.Views.project_ole_file import ProjectOleFile

def main(args: list) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The directory that contains your files.")
    args = parser.parse_args()
    # cd args.output
    # build a list of all bas, cls, frm, and frx files
    bas_files = glob.glob('*.bas')
    #cls_files = glob.glob('*.cls')
    #frm_files = glob.glob('*.frm')
    #frx_files = glob.glob('*.frx')

    # create a new project object
    project = VbaProject()

    # add default modules
    module = DocModule('Sheet1')
    module.addFile('src/vbaproject_compiler/blank_files/Sheet1.cls')
    project.addModule(module)
    module = DocModule('ThisWorkbook')
    module.addFile('src/vbaproject_compiler/blank_files/ThisWorkbook.cls')
    project.addModule(module)
    
    # add the files
    for file_path in bas_files:
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)
        code = StdModule(file[0])
        code.addFile(file_path)
        project.addModule(code)
    
    ole_file = ProjectOleFile(project)
    ole_file.write_file()
    
