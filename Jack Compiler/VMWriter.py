#for Nand2Tetris Part 2
#translates xml file into vm file

from pathlib import Path

class Symbol:
    classTable = {}
    methodTable = {}
    count = {"static":0, "this":0, "argument":0, "local":0}

    def add(self, name, symType, kind):
        classlevel = ["static", "this"]
        methodlevel = ["argument","local"]
        if kind not in classlevel+methodlevel:
            raise TypeError("not a valid kind")
        
        if kind in classlevel:
            if kind == "static":
                Symbol.classTable[name] = symType, kind, Symbol.count[kind]
                Symbol.count[kind]
        elif kind in methodlevel:
            if kind == "argument":
                Symbol.methodTable[name] = symType, kind, Symbol.count[kind]
                Symbol.count[kind]
                
    def varCount(self, kind):
        return Symbol.count[kind]

    def kindOf(self, name):
        if name in Symbol.methodTable:
            if Symbol.methodTable[name][1] == "argument":
                kind = "ARG"
            elif Symbol.methodTable[name][1] == "local":
                kind = "VAR"
        elif name in Symbol.classTable:
            if Symbol.classTable[name][1] == "static":
                kind = "STATIC"
            elif Symbol.classTable[name][1] == "this":
                kind = "FIELD"
        else:
            raise Exception("not found")
        return kind
    
    def typeOf(self, name):
        if name in Symbol.methodTable:
            return Symbol.methodTable[name][0]
        if name in Symbol.classTable:
            return Symbol.classTable[name][0]
        raise Exception("not found")
    
    def indexOf(self, name):
        if name in Symbol.methodTable:
            return Symbol.methodTable[name][2]
        if name in Symbol.classTable:
            return Symbol.classTable[name][2]
        raise Exception("not found")

def parseXML(file):
    filename = Path(file).stem
    with open(filename + '.xml', 'r')  as XMLFile:
        pass       

class XMLtokenizer:
    