#for Nand2Tetris Part2
#creates the .xml files 

#calls JackTokenizer for getting the token and writes it into .xml file

from JackTokenizer import *
from pathlib import Path


terminalElements = ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier']
operators = ['+', '-', '*', '/', '&', '|', '<', '>', '<=']

def compile(file = "new.jack"):
    tabs = 0
    filename = Path(file).stem
    encElem = []    # encountered elements

    tokenize(file)
    advance()
    
    with open(filename + '.xml', 'w') as XMLFile:
        lines = makeXMLCode().strip().split("\n")
        for line in lines:
            elementType = line.split()[0].strip("<>")
            # this is for making indentations
            if elementType not in terminalElements:
                if len(encElem) != 0 and elementType.strip("/") == encElem[-1]:
                    tabs -= 1
                    encElem.pop()

            XMLFile.write("\t"*tabs + line + "\n")

            # this is for making indentations
            if elementType not in terminalElements:
                if elementType[0] != "/":
                    tabs += 1
                    encElem.append(elementType)

#TODO: to be continued    
def makeXMLCode():
    return compileLet()

def compileLet():
    output = "<letStatement>\n"
    output += "<keyword> " + keyword() + " </keyword>\n"
    advance()
    output += "<identifier> " + identifier() + " </identifier>\n"
    advance()
    if symbol() == "[":
        output += "<symbol> " + symbol() + " </symbol>\n"
        advance()
        output += compileExpression()
        advance()
        output += "<symbol> " + symbol() + " </symbol>\n"
        advance()
    output += "<symbol> " + symbol() + " </symbol>\n"
    advance()
    output += compileExpression()
    advance()
    output += "<symbol> " + symbol() + " </symbol>\n"
    output += "</letStatement>\n"
    return output

# term (op term)*
# x is an expression
# x = [(something), something] <- can be with brackets or no brackets
def compileExpression():
    output = ""
    openbracket = False
    if tokenType() == "SYMBOL" and symbol() == "(":
        output += "<symbol> " + symbol() + " </symbol>\n"
        openbracket = True
        advance()
    output += "<expression>\n"

    output += compileTerm()
    advance()
    if tokenType() == "SYMBOL" and symbol() in operators:
        output += "<symbol> " + symbol() + " </symbol>\n"
        advance()
        output += compileTerm()
    else: 
        goback()

    output += "</expression>\n"
    advance()
    if tokenType() == "SYMBOL" and symbol() == ")" and openbracket:
        output += "<symbol> " + symbol() + " </symbol>\n" 
        openbracket = False
    else:
        goback()
    return output

# keywordConstant = ['true', 'false', 'none', 'this']
# term_options = integerConstant, stringConstant, keywordConstant, unaryOp term,
#                varName, varName [ expression ], subroutineCall, ( expression )
def compileTerm():
    output = "<term>\n"

    if tokenType() == "INT_CONST":
        output += "<integerConstant> " + intVal() + " </integerConstant>\n"
    elif tokenType() == "STRING_CONST":
        output += "<stringConstant> " + strVal() + " </stringConstant>\n"
    elif tokenType() == "KEYWORD":
        output += "<keywordConstant> " + keyword() + " </keywordConstant>\n"
    elif tokenType() == "IDENTIFIER":
        output += "<identifier> " + identifier() + " </identifier>\n"
    elif tokenType() == "SYMBOL" and symbol() == "(":
        output += compileExpression()     

    output += "</term>\n"
    return output



compile()  