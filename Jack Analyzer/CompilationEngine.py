#for Nand2Tetris Part2
#creates the .xml files 

#calls JackTokenizer for getting the token and writes it into .xml file

from JackTokenizer import *
from pathlib import Path

tokenize("Jack Analyzer/new.jack")
for token in tokens:
    advance()
    print(tokenType())
