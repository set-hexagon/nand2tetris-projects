#for Nand2Tetris Part2
#creates the .xml files 

#calls JackTokenizer for getting the token and writes it into .xml file

from JackTokenizer import *
from pathlib import Path


terminalElements = ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier', 'keywordConstant']
operators = ['+', '-', '*', '/', '&', '|', '<', '>', '<=']

def compile(file = "new.jack"):
    tabs = 0
    filename = Path(file).stem
    encElem = []    # encountered elements

    tokenize(file)
    advance()
    
    with open(filename + '.xml', 'w') as XMLFile:
        lines = compileClass().strip().split("\n")
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

classVarDecType = ["static", "field"]
subroutineDecType = ["constructor", "function", "method"]
# 'class' className '{'classVarDec* subroutineDec*'}'
def compileClass():
    output = "<class>\n"
    output += printKeyword()
    advance()
    output += printIdentifier()
    advance()
    output += printSymbol()
    advance()
    while tokenType() == "KEYWORD" and keyword() in classVarDecType:
        output += compileClassVarDec()
        advance()
    while tokenType() == "KEYWORD" and keyword() in subroutineDecType:
        output += compileSubroutine()
        advance() 
    output += printSymbol()
    output += "</class>\n"
    return output


#('static'|'field) type varName(','varName)*';'
def compileClassVarDec():
    output = "<classVarDec>\n"
    output += printKeyword()
    advance()
    output += printType()
    advance()
    output += printIdentifier()
    advance()
    while tokenType() == "SYMBOL" and symbol() == ",":
        output += printSymbol()
        advance()
        output += printIdentifier()
        advance()
    output += printSymbol()
    output += "</classVarDec>\n"
    print(output)
    return output

#('construnctor'|'function'|'method') ('void'|type) subroutineName'('parameterList')' subroutineBody
def compileSubroutine():
    output = "<subroutineDec>\n"
    output += printKeyword()
    advance()
    if tokenType() == "KEYWORD" and keyword() == "void":
        output += printKeyword()
    else:
        output += printType()
    advance()
    output += printIdentifier() 
    advance()
    output += printSymbol()
    advance()
    output += compileParameterList()
    advance()
    output += printSymbol()
    advance()
    output += compileSubroutineBody()
    output += "</subroutineDec>\n"
    print(output)
    return output

#((type varName)(',' type varName)*)?
def compileParameterList():
    output = "<parameterList>\n"
    if tokenType() == "KEYWORD":
        output += printKeyword()
        advance()
        output += printIdentifier()
        advance()
        while tokenType() == "SYMBOL" and symbol() == ",":
            output += printSymbol()
            advance()
            output += printKeyword()
            advance()
            output += printIdentifier()
            advance()
    retreat()
    output += "</parameterList>\n"
    print(output)
    return output 

#'{'varDec* statements'}'
def compileSubroutineBody():
    output = "<subroutineBody>\n"
    print("hey",tokens[token_no-2],tokens[token_no])
    output += printSymbol()
    
    advance()
    while tokenType() == "KEYWORD" and keyword() == "var":
        output += compileVarDec()
        advance()
    output += compileStatements()
    advance()

    output += printSymbol()
    output += "</subroutineBody>\n"
    print(output)
    return output

# 'var' type varName (',' varName)*;
def compileVarDec():
    output = "<VarDec>\n"
    output += printKeyword()
    advance()
    output += printType()
    advance()
    output += printIdentifier()
    advance()
    while tokenType() == "SYMBOL" and symbol() == ",":
        output += printSymbol()
        advance()
        output += printIdentifier()
        advance()
    output += printSymbol()
    output += "</VarDec>\n"
    print(output)
    return output

# statements = statement*
# statement = letStatement|ifStatement|whileStatement|doStatement|returnStatement
statementTypes = ["let", "if", "while", "do", "return"]
def compileStatements():
    output = "<statements>\n"
    while tokenType() == "KEYWORD" and keyword() in statementTypes:
        if keyword() == "let":
            output += compileLet()
        elif keyword() == "if":
            output += compileIf()
        elif keyword() == "while":
            output += compileWhile()
        elif keyword() == "do":
            output += compileDo()
        elif keyword() == "return":
            output += compileReturn()
        advance()
    retreat()
    output += "</statements>\n"
    print(output)
    return output

# 'let' varName('['expression']')? '=' expression;
def compileLet():
    output = "<letStatement>\n"
    output += printKeyword()
    advance()
    output += printIdentifier()
    advance()
    if symbol() == "[":
        output += printSymbol()
        advance()
        output += compileExpression()
        advance()
        output += printSymbol()
        advance()
    output += printSymbol()
    advance()
    output += compileExpression()
    advance()
    output += printSymbol()
    output += "</letStatement>\n"
    print(output)
    return output

# 'if' '('expression')''{'statements'}' ('else')'{'statements'}')?
def compileIf():
    output = "<ifStatement>\n"
    output += printKeyword()
    advance()
    output += printSymbol()
    advance()
    output += compileExpression()
    advance()
    output += printSymbol()
    advance()
    output += printSymbol()
    advance()
    output += compileStatements()
    advance()
    output += printSymbol()
    advance()
    if tokenType() == "KEYWORD" and keyword() == 'else':
        output += printKeyword()
        advance()
        output += printSymbol()
        advance()
        output += compileStatements()
        advance()
        output += printSymbol()
    else:
        retreat()
    output += "</ifStatement>\n"
    print(output)
    return output

# 'while' '('expression')''{'statements'}'
def compileWhile():
    output = "<whileStatement>\n"
    output += printKeyword()
    advance()
    output += printSymbol()
    advance()
    output += compileExpression()
    advance()
    output += printSymbol()
    advance()
    output += printSymbol()
    advance()
    output += compileStatements()
    advance()
    output += printSymbol()
    output += "</whileStatement>\n"
    print(output)
    return output

# 'do' subroutineCall';'
def compileDo():
    output = "<doStatement>\n"
    output += printKeyword()
    advance()
    output += compileSubroutineCall()
    advance()
    output += printSymbol()
    output += "</doStatement>\n"
    print(output)
    return output

# 'return' expression?';'
def compileReturn():
    output = "<returnStatement>\n"
    output += printKeyword()
    advance()
    if not (tokenType() == "SYMBOL" and symbol() == ";"):
        output += compileExpression()
        advance()
    output += printSymbol()    
    output += "</returnStatement>\n"
    print(output)
    return output

# subroutineName'('expressionList')'|(className|varName)'.'subroutineName'('expressionList')'
def compileSubroutineCall():
    output = printIdentifier()
    advance()
    output += printSymbol()
    if symbol() == "(":
        advance()
        output += compileExpressionList()
        advance()
        output += printSymbol()
    elif symbol() == ".":
        advance()
        output += compileSubroutineCall()
    print(output)
    return output

# term (op term)*
# if x is an expression
# x = [(something), something] <- can be with brackets or no brackets
def compileExpression():
    output = ""
    openbracket = False
    if tokenType() == "SYMBOL" and symbol() == "(":
        output += printSymbol()
        openbracket = True
        advance()
    output += "<expression>\n"

    output += compileTerm()
    advance()
    if tokenType() == "SYMBOL" and symbol() in operators:
        output += printSymbol()
        advance()
        output += compileTerm()
    else: 
        retreat()

    output += "</expression>\n"
    advance()
    if tokenType() == "SYMBOL" and symbol() == ")" and openbracket:
        output += printSymbol()
        openbracket = False
    else:
        retreat()
    print(output)
    return output

# keywordConstant = ['true', 'false', 'none', 'this']
# term_options = integerConstant, stringConstant, keywordConstant, unaryOp term,
#                varName, varName [ expression ], subroutineCall, ( expression )
unaryOp = ['-','~']
def compileTerm():
    output = "<term>\n"

    if tokenType() == "INT_CONST":
        output += printIntegerConstant()
    elif tokenType() == "STRING_CONST":
        output += printStringConstant()
    elif tokenType() == "KEYWORD":
        output += printKeywordConstant()
    elif tokenType() == "IDENTIFIER":
        output += printIdentifier()

        # for varName[expression] i.e. list and varName(expressionList) i.e. subroutine
        advance()
        if tokenType() == "SYMBOL" and symbol() == "[":
            output += printSymbol()
            advance()
            output += compileExpression()
            advance()
            output += printSymbol()
        elif tokenType() == "SYMBOL" and symbol() == "(":
            output += compileSubroutine()
        else: 
            retreat() 


    elif tokenType() == "SYMBOL" and symbol() == "(":
        output += compileExpression()     
    elif tokenType() == "SYMBOL" and symbol() in unaryOp:
        output += printSymbol() 
        advance()
        output += compileTerm()

    output += "</term>\n"
    print(output)
    return output

# (expression(','expression)*)?
def compileExpressionList():
    output = "<expressionList>\n"
    if not (tokenType() == "SYMBOL" and symbol() == ")"):
        output += compileExpression()
        advance()
        while tokenType() == "SYMBOL" and symbol() == ",":
            output += printSymbol()
            advance()
            output += compileExpression()
            advance()
        retreat()
    else:
        retreat()
    output += "</expressionList>\n"
    print(output)
    return output


# helper functions for minimizing repeated stuff
# outputs the xml code for some of the repeated stuff
def printKeywordConstant():
    return "<keywordConstant> " + keyword() + " </keywordConstant>\n"
def printStringConstant():
    return "<stringConstant> " + strVal() + " </stringConstant>\n"
def printIntegerConstant():
    return "<integerConstant> " + str(intVal()) + " </integerConstant>\n"
def printKeyword():
    return "<keyword> " + keyword() + " </keyword>\n"
def printIdentifier():
    return "<identifier> " + identifier() + " </identifier>\n"
def printSymbol():
    return "<symbol> " + symbol() + " </symbol>\n"
def printType():
    if tokenType() == "KEYWORD":
        return "<keyword> " + keyword() + " </keyword>\n"
    elif tokenType() == "IDENTIFIER":
        return "<identifier> " + identifier() + " </identifier>\n"

compile()  