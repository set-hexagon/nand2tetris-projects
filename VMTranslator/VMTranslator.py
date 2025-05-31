#for Nand2Tetris Part2
#translates VM code to assembly
#assumes the VM code is correct

#pass VM code file as CLA, output assembly file will be generated with the fileName.asm
#pass folder containg VM files, output will have one file with folderName.asm

#* if AttributeError: 'list' object has no attribute 'split' happens :: code writer encountered something unexpected
import sys
import os
from pathlib import Path
from Parser import *
import CodeWriter

if __name__ == "__main__":
    path = sys.argv[1]

    if os.path.isfile(path):
        # writes bootstrap code
        with open(Path(path).stem + ".asm", 'w') as AssCode:
            bootstrap_code = ("//bootstrap_code "
                              "@256 D=A @SP M=D "                             # SP = 256
                              ).split()    
            for bootstrap in bootstrap_code:
                AssCode.write(bootstrap + "\n")
            AssCode.write("\n")

        parse(path, 'a', path)


    elif os.path.isdir(path):
        mode = 'a'
        folder = Path(path).name

        # writes bootstrap code
        with open(folder + ".asm", 'w') as AssCode:
            bootstrap_code = ("//bootstrap_code "
                              "@256 D=A @SP M=D " +                             # SP = 256
                            CodeWriter.translate("call Sys.init 0", folder)     # call Sys.init
                              ).split()    
            for bootstrap in bootstrap_code:
                AssCode.write(bootstrap + "\n")
            AssCode.write("\n")

        for file in Path(path).rglob('*'):
            if file.is_file() and file.suffix == ".vm":
                #makes a single file from multiple files 
                #the multiple files are treated as different classes
                parse(file, mode, folder)
                mode = 'a'
