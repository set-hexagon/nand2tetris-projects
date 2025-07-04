import Parser
from collections import defaultdict

labels = {}
run_i = defaultdict(int)
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
        
        elif seg == "pointer":
            # pointer 0 => POP THIS
            # pointer 1 => POP THAT
            if line[2] == "0": assline = "@SP M=M-1 A=M D=M @THIS M=D"
            if line[2] == "1": assline = "@SP M=M-1 A=M D=M @THAT M=D"
        
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
            
        elif seg == "pointer":
            # pointer 0 => push THIS
            # pointer 1 => push THAT
            if line[2] == "0": assline = "@THIS D=M @SP A=M M=D @SP M=M+1"
            if line[2] == "1": assline = "@THAT D=M @SP A=M M=D @SP M=M+1"
            
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
                       "@SP M=M-1 A=M D=D-M "       # x-y != 0: goto NOTZERO
                       "@NOTZERO D;JGT "
                       "@SP A=M M=1 @ENDEQ 0;JMP "  # x-y == 0: RAM[SP] = 1 , goto ENDEQ
                       "(NOTZERO) "
                       "@SP A=M M=0 "               # RAM[SP] = 0
                       "(ENDEQ) "
                       "@SP M=M+1")                 # SP++
        
        elif line[0] == "gt":
            assline = ("@SP M=M-1 A=M D=M "         # SP--
                       "@SP M=M-1 A=M D=M-D "       # D = x-y != 0: goto GREATER
                       "@GREATER D;JGT "  
                       "@SP A=M M=0 @ENDGT 0;JMP "  # if x-y < 0 RAM[SP] = 0, goto ENDGT
                       "(GREATER) "
                       "@SP A=M M=1 "               # if x-y > 0 RAM[SP] = 1
                       "(ENDGT) "
                       "@SP M=M+1")                 # SP++
            
        elif line[0] == "lt":
            assline = ("@SP M=M-1 A=M D=M "         # SP--
                       "@SP M=M-1 A=M D=M-D "       # D = x-y != 0: goto NOTLESS
                       "@NOTLESS D;JGT "  
                       "@SP A=M M=1 @ENDLT 0;JMP "  # if x-y < 0 RAM[SP] = 1, goto ENDLT
                       "(NOTLESS) "
                       "@SP A=M M=0 "               # if x-y > 0 RAM[SP] = 0
                       "(ENDLT) "
                       "@SP M=M+1")                 # SP++
            
        elif line[0] == "and":
            assline = ("@SP M=M-1 A=M D=M "         # SP--
                       "@AND D;JEQ "                # if y=0: goto AND
                       "@SP M=M-1 A=M D=M "         
                       "@AND D;JEQ "                # if x=0: goto AND
                       "@SP A=M M=1 @ENDAND 0;JMP " # if x and y != 0: RAM[SP] = 1
                       "(AND) "
                       "@SP A=M M=0 "                # RAM[SP] = 0
                       "(ENDAND) "     
                       "@SP M=M+1")                 # SP++
             
        elif line[0] == "or":
            assline = ("@SP M=M-1 A=M D=M "         # SP--
                       "@OR D;JNE "                 # if y!=0: goto OR
                       "@SP M=M-1 A=M D=M "       
                       "@OR D;JNE "                 # if x!=0; goto OR
                       "@SP A=M M=0 @ENDOR 0;JMP "  # if x and y are 0 RAM[SP] = 0
                       "(OR) "
                       "@SP A=M M=1 "               # RAM[SP] = 1
                       "(ENDOR) "
                       "@SP M=M+1")                 # SP++
            
        elif line[0] == "not":
            assline = ("@SP M=M-1 A=M D=M "         # SP--
                       "@ZERO D;JEQ "               # if y == 0: goto ZERO
                       "@SP A=M M=0 @ENDNOT 0;JMP " # if y != 0: y = 0
                       "(ZERO) "
                       "@SP A=M M=1 "               # if y == 0: y = 1
                       "(ENDNOT) "
                       "@SP M=M+1")                 # SP++
        

    elif Parser.cmdType(line) == "C_LABEL":
        assline = f"({line[1]})"
    
    elif Parser.cmdType(line) == "C_GOTO":
        assline = f"@{line[1]} 0;JMP"
    
    elif Parser.cmdType(line) == "C_IF":
        assline = ("@SP M=M-1 A=M D=M "              
                   f"@{line[1]} D;JGT"          # if RAM[SP-1] > 0 : jump to label
                    )
        
    elif Parser.cmdType(line) == "C_CALL":
        foo = line[1]
        nArgs = line[2]
        ret_addr = f"{foo}$ret.{Parser.lineno[filename]}"

        assline = (f"@{ret_addr} D=A @SP A=M M=D @SP M=M+1 "         # push return_address
                   "@LCL D=M @SP A=M M=D @SP M=M+1 "                 # push LCL
                   "@ARG D=M @SP A=M M=D @SP M=M+1 "                 # push ARG
                   "@THIS D=M @SP A=M M=D @SP M=M+1 "                # push THIS
                   "@THAT D=M @SP A=M M=D @SP M=M+1 "                # push THAT
                   f"@SP D=M @{nArgs} D=D-A @5 D=D-A @ARG M=D "      # ARG = SP - nArgs - 5
                   "@SP D=M @LCL M=D "                               # LCL = SP
                   f"@{foo} 0;JMP "                                  # goto function
                   f"({ret_addr})"                                   # return_address label
                   )    
        
    elif Parser.cmdType(line) == "C_FUNCTION":
        foo = line[1]
        nVars = int(line[2])

        assline = f"({foo}) "                        # function label
        for i in range(nVars):
            assline += "@SP A=M M=0 @SP M=M+1 "      # inserting nVars 0 in the stack

    elif Parser.cmdType(line) == "C_RETURN":
        assline = ("@LCL D=M @endFrame M=D "                     # endFrame = LCL
                   "@5 D=D-A A=D D=M @retAddr M=D "              # retAddr = *(endFrame - 5)
                   "@SP M=M-1 A=M D=M @ARG A=M M=D "             # ARG = pop() - puts the return value in ARG
                   "@ARG D=M+1 @SP M=D "                         # SP = ARG + 1
                   "@endFrame D=M @1 D=D-A A=D D=M @THAT M=D "   # THAT = *(endFrame - 1)
                   "@endFrame D=M @2 D=D-A A=D D=M @THIS M=D "   # THIS = *(endFrame - 2)
                   "@endFrame D=M @3 D=D-A A=D D=M @ARG M=D "    # ARG = *(endFrame - 3)
                   "@endFrame D=M @4 D=D-A A=D D=M @LCL M=D "    # LCL = *(endFrame - 4)
                   "@retAddr A=M 0;JMP"
                   )         
        
    return assline