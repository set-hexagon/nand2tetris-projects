#for Nand2Tetris Part2
#translates JackCode into tokens for easier compilation
#assumes Jack Code is correct

#pass .jack file as CLA, output .xml file will be generated with the same name
#pass folder containing .jack files, output will have one .xml file for every .jack file

import sys
import os
from pathlib import Path
from CompilationEngine import *
from JackAnalyzer import *

if __name__ == "__main__":
    path = sys.argv[1]

    if os.path.isfile(path):
        exit(0)

    elif os.path.isdir(path):
        exit(0)