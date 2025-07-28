#for Nand2Tetris Part 2
#tokenizes the .jack file
#assumes the jack file is correct

#called by compilation engine, opens the file and returns a token
#skips comments and whitespaces

from pathlib import Path
import sys

tokenType = ['keyword', 'symbol', 'identifier','int_const', 'var']

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

# initializer
# returns a list of the tokens in a .jack file
def tokenize(file):
    global tokens
    with open(file, 'r') as JackFile:
        for line in JackFile:
            line = line.strip().split()
            for word in line:
                if word in keywords:
                    tokens.append(word)
                elif word in symbols:
                    tokens.append(word)
                else:
                    tokens += moretokenize(word)

# helper for the tokenize function
# tokenizes the strings containing identifiers or constants
def moretokenize(word):
    temp_token = []
    buff = ''
    i = 0
    while i < len(word):
        c = word[i]
        if c in symbols:
            temp_token.append(c)
            i += 1

        elif c.isalpha() or c == "\"":
            buff += c
            i += 1
            while i < len(word):
                c = word[i]
                if c.isalnum() or c == "\"":
                    buff += c
                else:                    
                    break
                i += 1
            temp_token.append(buff) 
            buff = ''

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
        sys.exit("invalid use of function")

def symbol():
    if tokenType() == "SYMBOL":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function")

def identifier():
    if tokenType() == "IDENTIFIER":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function")

def intVal():
    if tokenType() == "INT_CONST":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function")

def strVal():
    if tokenType() == "STRING_CONST":
        return tokens[token_no]
    else:
        sys.exit("invalid use of function")
