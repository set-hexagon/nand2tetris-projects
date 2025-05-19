import Parser

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
            
    elif Parser.cmdType(lineRaw) == "C_ARITHMETIC":
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