import argparse
import glob
import os
from vbaproject_compiler.vbaProject import VbaProject
from vbaproject_compiler.Models.Entities.doc_module import DocModule
from vbaproject_compiler.Models.Entities.std_module import StdModule
from vbaproject_compiler.Views.project_ole_file import ProjectOleFile


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The directory that contains your files.")
    args = parser.parse_args()
    # cd args.output
    # build a list of all bas, cls, frm, and frx files
    bas_files = glob.glob('/*.bas', root_dir=args.directory)
    # cls_files = glob.glob('*.cls')
    # frm_files = glob.glob('*.frm')
    # frx_files = glob.glob('*.frx')

    # create a new project object
    project = VbaProject()

    # add default modules
    module = DocModule('Sheet1')
    base_path = os.path.basename(__file__)
    module.add_file(base_path + '/blank_files/Sheet1.cls')
    project.add_module(module)
    module = DocModule('ThisWorkbook')
    module.add_file(base_path + '/blank_files/ThisWorkbook.cls')
    project.add_module(module)

    # add the files
    for file_path in bas_files:
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)
        code = StdModule(file[0])
        code.add_file(file_path)
        project.add_module(code)
    os.mkdir('project')
    ole_file = ProjectOleFile(project)
    ole_file.write_file()
    file = glob.glob('vbaProject.bin')


main()
