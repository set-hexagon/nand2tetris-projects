import CodeWriter
from collections import defaultdict
from pathlib import Path

lineno = defaultdict(int)
#goes through file line by line and makes another file with same name
def parse(file, mode):
    filename = Path(file).stem
    with open(file, 'r') as VMCode, open(filename + ".asm", mode) as AssCode:

        #goes through the code line by line
        line = VMCode.readline()
        while line:
            if checkCode(line):                    #checks if the read line is not a whitespace or comment
                lineno[filename] += 1
                ass = CodeWriter.translate(line,filename).split()      
                
                AssCode.write("\n//" + line)       #writes the VM line
                if line[-1] !=  '\n' : AssCode.write("\n")      #last lines don't have \n

                for a in ass:
                    AssCode.write(a)               #writes the assembly line
                    AssCode.write("\n")

            elif line.startswith('//'):
                AssCode.write(line + "\n")         #writes the comments


            line = VMCode.readline() 


#checks if the read line is not a whitespace or comment
def checkCode(line):
    if line.startswith("\n") or line.startswith("//"):
        return False
    
    return True

#returns the command type
def cmdType(line):
    if type(line) == str:
        line = line.split()

    arithmeticOrLogic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    if line[0] in arithmeticOrLogic:
        return "C_ARITHMETIC"
    elif line[0] == "push":
        return "C_PUSH"
    elif line[0] == "pop":
        return "C_POP"
    elif line[0] == "label":
        return "C_LABEL"
    elif line[0] == "goto":
        return "C_GOTO"
    elif line[0] == "if-goto":
        return "C_IF"
    elif line[0] == "function":
        return "C_FUNCTION"
    elif line[0] == "call":
        return "C_CALL"
    elif line[0] == "return":
        return "C_RETURN"

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