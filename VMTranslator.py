#for Nand2Tetris Part2
#translates VM code to assembly
#assumes the VM code is correct

#pass VC code file as CLA, output assembly file will be generated with the sameName.asm
import sys
import os

def translate(lineRaw,filename):
    assline = []
    line = lineRaw.split()

    segments = {"local":"LCL", "argument": "ARG","this": "THIS", "that":"THAT", "static":"STATIC", "temp":"temp"}

    if line[0] == 'pop':
        seg = line[1]
        i = line[2]

        if seg in ["local", "argument", "this", "that"]:
            # addr = seg_pointer + i
            # SP--
            # RAM[addr] = RAM[SP]
            assline = (f"@{i} D=A @addr M=D @{segments[seg]} D=M @addr M=D+M "
                        "@SP M=M-1 A=M D=M "
                        "@addr A=M M=D"
                        )
            
        elif seg == "static":
            # SP--
            # filename.i = RAM[SP]
            assline = ( "@SP M=M-1 A=M D=M "
                       f"@{filename}.{i} M=D"
                       )
            
        elif seg == "temp":
            # addr = 5 + i
            # SP--
            # RAM[addr] = RAM[SP]
            assline = (f"@{i} D=A @addr M=D @5 D=A @addr M=D+M "
                        "@SP M=M-1 A=M D=M "
                        "@addr A=M M=D"
                        )
        
    elif line[0] == 'push':
        seg = line[1]
        i = line[2]

        if seg in ["local", "argument", "this", "that"]:
            # addr = seg_pointer + i
            # RAM[SP] = RAM[addr]
            # SP++
            assline = (f"@{i} D=A @addr M=D @{segments[seg]} D=M @addr M=D+M "
                        "@addr A=M D=M "
                        "@SP A=M M=D "
                        "@SP M=M+1"
                        )
        
        elif seg == "constant":
            # RAM[SP] = i
            # SP++
            assline = (f"@{i} D=A @SP A=M M=D "
                        "@SP M=M+1"
                        )
            
        elif seg == "static":
            # RAM[SP] = filename.i
            # SP++
            assline = (f"@{filename}.{i} D=M @SP A=M M=D "
                        "@SP M=M+1"
                        )
            
        elif seg == "temp":
            # addr = 5 + i
            # RAM[SP] = RAM[addr]
            # SP++
            assline = (f"@{i} D=A @addr M=D @5 D=A @addr M=D+M "
                       "@addr A=M D=M "
                        "@SP A=M M=D "
                        "@SP M=M+1"
                        )
            
    elif cmdType(lineRaw) == "C_ARITHMETIC":
        if line[0] == "add":
            assline = ("@SP M=M-1 A=M D=M "     # SP-- 
                       "@SP M=M-1 A=M M=D+M "   # x + y
                       "@SP M=M+1")             # SP++
            
        elif line[0] == "sub":
            assline = ("@SP M=M-1 A=M D=M "     # SP-- 
                       "@SP M=M-1 A=M M=M-D "   # x - y
                       "@SP M=M+1")             # SP++
            
        elif line[0] == "neg":
            assline = ("@SP M=M-1 A=M "         # SP--
                       "M=-M "                  # y = -y
                       "@SP M=M+1")             # SP++
        
        elif line[0] == "eq":
            assline = ("@SP M=M-1 A=M D=M "         # SP--
                       "@SP M=M-1 A=M D=D-M M=!D "  # x == y ? 1 : 0
                       "@SP M=M+1")                 # SP++
        
        elif line[0] == "gt":
            assline = ("@SP M=M-1 A=M D=M "     # SP--
                       "@SP M=M-1 A=M D=M-D "   # D = x-y
                       "@GREATER D;JGT "  
                       "@SP A=M M=0 "           # if x-y < 0 RAM[SP] = 0
                       "(GREATER) "
                       "@SP A=M M=1 "           # if x-y > 0 RAM[SP] = 1
                       "@SP M=M+1")             # SP++
            
        elif line[0] == "lt":
            assline = ("@SP M=M-1 A=M D=M "     # SP--
                       "@SP M=M-1 A=M D=M-D "   # D = x-y
                       "@GREATER D;JGT "  
                       "@SP A=M M=1 "           # if x-y < 0 RAM[SP] = 1
                       "(GREATER) "
                       "@SP A=M M=0 "           # if x-y > 0 RAM[SP] = 0
                       "@SP M=M+1")             # SP++
            
        elif line[0] == "and":
            assline = ("@SP M=M-1 A=M D=M "     # SP--
                       "@SP M=M-1 A=M M=D&M "   # x = x & y
                       "@SP M=M+1")             # SP++
             
        elif line[0] == "or":
            assline = ("@SP M=M-1 A=M D=M "     # SP--
                       "@SP M=M-1 A=M M=D|M "   # x = x | y
                       "@SP M=M+1")             # SP++
            
        elif line[0] == "not":
            assline = ("@SP M=M-1 A=M "         # SP--
                       "M=!M "                  # y = !y
                       "@SP M=M+1")             # SP++
        
    return assline
    

#checks if the read line is not a whitespace or comment
def checkCode(line):
    if line.startswith("\n") or line.startswith("//"):
        return False
    
    return True

#returns the command type
def cmdType(line):
    line = line.split()

    arithmeticOrLogic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    if line[0] in arithmeticOrLogic:
        return "C_ARITHMETIC"
    elif line[0] == "push":
        return "C_PUSH"
    elif line[0] == "pop":
        return "C_POP"

#returns the first argument
def arg1(line):
    type = cmdType(line)

    if type == "C_RETURN": exit(1)

    line = line.split()
    if type == "C_ARITHMETIC":
        return line[0]
    return line[1]

#returns the second argument
def arg2(line):
    type = cmdType(line)    

    validTypes = ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]
    if type in validTypes:
        line = line.split()
        return line[2]
    else: exit(1)

#goes through file line by line and makes another file with same name
def parse(file):
    with open(file, 'r') as VMCode, open(file.strip(".vm") + ".asm", 'w') as AssCode:
        filename = file.strip(".vm")

        #goes through the code line by line
        line = VMCode.readline()
        while line:
            if checkCode(line):                    #checks if the read line is not a whitespace or comment
                ass = translate(line,filename).split()      
                
                AssCode.write("\n//" + line)       #writes the VM line
                for a in ass:
                    AssCode.write(a)               #writes the assembly line
                    AssCode.write("\n")

            elif line.startswith('//'):
                AssCode.write(line + "\n")         #writes the comments


            line = VMCode.readline() 

if __name__ == "__main__":
    path = sys.argv[1]
    if os.path.isfile(path):
        parse(path)