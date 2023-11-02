import argparse

def main(args: list) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The directory that contains your files.")
    parser.add_argument("-o", "--output",
                        help="The output file name.")
    args = parser.parse_args()
    # cd args.output
    # build a list of all bas, cls, frm, and frx files
    # create a new project object
    # add the files
    # create the output directory
    # save the deliverables.
