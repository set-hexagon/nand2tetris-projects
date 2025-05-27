#for Nand2Tetris Part2
#translates VM code to assembly
#assumes the VM code is correct

#pass VC code file as CLA, output assembly file will be generated with the sameName.asm
import sys
import os
from pathlib import Path
from Parser import *

if __name__ == "__main__":
    path = sys.argv[1]
    if os.path.isfile(path):
        parse(path, 'w')
    
    elif os.path.isdir(path):
        mode = 'w'
        for file in Path(path).rglob('*'):
            if file.is_file() and file.endswith(".vm"):
                #makes a single file from multiple files 
                #the multiple files are treated as different classes
                parse(file, mode)
                mode = 'a'
