#for Nand2Tetris Part 2
#tokenizes the .jack file
#assumes the jack file is correct

#called by compilation engine, opens the file and returns a token
#skips comments and whitespaces

#TODO: add symbol table

from pathlib import Path
import sys
import re

tokenTypes = ['keyword', 'symbol', 'identifier','int_const', 'var']

keywords = [
    'class', 'constructor', 'function', 'method', 'field', 'static',
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
    'this', 'let', 'do', 'if', 'else', 'while', 'return'
]

symbols = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
    '&', '|', '<', '>', '=', '~'
]

tokens = []
strConst = False
strBuff = ''

#TODO: string literals can't contain blank spaces
# initializer
# returns a list of the tokens in a .jack file
def tokenize(file):
    global tokens, strConst, strBuff
    mLineCmt = False
    sLineCmt = False
    with open(file, 'r') as JackFile:
        for line in JackFile:
            line = line.strip().split()
            for word in line:
                #ignoring comments
                if word.startswith("//"): sLineCmt = True
                elif word.startswith("/*"): mLineCmt = True
                if word.endswith("*/"):
                    mLineCmt = False
                    continue
                if mLineCmt or sLineCmt == True: continue

                if word in keywords:
                    tokens.append(word)
                elif word in symbols:
                    tokens.append(word)
                else:
                    tokens += moretokenize(word)
            sLineCmt = False
    print(tokens)

# helper for the tokenize function
# tokenizes the strings containing identifiers or constants
# goes throught the string one letter at a time and adds it to a buffer depending on whether it's alnum, numeric or symbol
def moretokenize(word):
    global strConst, strBuff
    temp_token = []
    buff = ''
    i = 0
    while i < len(word):
        c = word[i]
        # a symbol is just a token so append it to the list
        if c in symbols:
            temp_token.append(c)
            i += 1

        # for StringConstant
        elif c == "\"" or strConst:
            strConst = not strConst
            strBuff += c
            i += 1
            while i < len(word):
                c = word[i]
                strBuff += c
                if c == "\"":
                    i += 1
                    break
                i += 1
            temp_token.append(buff)
            buff = ''

        # for identifiers which can start only with alphabets or _ but can contain numbers in them
        elif c.isalpha() or c == "_":
            # Start of identifier
            buff += c
            i += 1
            while i < len(word):
                c = word[i]
                if c.isalnum() or c == "_":
                    buff += c
                    i += 1
                else:
                    break
            temp_token.append(buff)
            buff = ''

        # for IntegerConstant
        elif c.isnumeric():
            buff += c
            i += 1
            while i < len(word):
                c = word[i]
                if c.isnumeric():
                    buff += c
                else:
                    break
                i += 1
            temp_token.append(buff)
            buff = ''

        else:
            i += 1

    return temp_token

token_no = -1   # index for tokens[]
def hasMoreTokens():
    if token_no < len(tokens) - 1:
        return True
    return False

def advance():
    global token_no
    token_no += 1
def retreat():
    global token_no
    token_no -= 1

def tokenType():
    token = tokens[token_no]
    if token in keywords:
        return "KEYWORD"
    elif token in symbols:
        return "SYMBOL"
    elif token.isnumeric():
        return "INT_CONST"
    elif token.startswith("\"") and token.endswith("\""):
        return "STRING_CONST"
    else:
        return "IDENTIFIER"


def keyword():
    if tokenType() == "KEYWORD":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function - keyword")

def symbol():
    if tokenType() == "SYMBOL":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function - symbol " )

def identifier():
    if tokenType() == "IDENTIFIER":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function - identifier")

def intVal():
    if tokenType() == "INT_CONST":
        return int(tokens[token_no])
    else:
        sys.exit("invalid use of function - int_const")

def strVal():
    if tokenType() == "STRING_CONST":
        return tokens[token_no].strip("\"")
    else:
        sys.exit("invalid use of function - string_const")


