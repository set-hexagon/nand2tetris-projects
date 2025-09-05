#for Nand2Tetris Part2
#compilers the jack code
#assumes Jack Code is correct

#pass .jack file as CLA, output .vm file will be generated with the same name
#pass folder containing .jack files, output will have one .vm file for every .jack file
#TODO: make optional CLA for outputing .xml files too

import sys
import os
from pathlib import Path
from CompilationEngine import *

if __name__ == "__main__":
    path = sys.argv[1]
    if os.path.isfile(path):
        compile(path)

    elif os.path.isdir(path):
        for file in Path(path).rglob("*"):
            if file.is_file() and file.suffix == ".jack":
                compile(file)