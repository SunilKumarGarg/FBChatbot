import sys, os

sys.path.append('JSGFTools')

from deterministicGenerator import DeterministicGenerator
import JSGFParser as parser

grammarFilePath = []
for path, dirs, files in os.walk("Data"):
    for f in files:
        if ".gram" in f:
            grammarFilePath.append(path+"/"+f)


for f in grammarFilePath:
    fileStream = open(f)
    grammar = parser.getGrammarObject(fileStream)
    processor = DeterministicGenerator(grammar)

    #create training files
    dir,_ = os.path.split(os.path.abspath(f))
    trainingFile = open(dir+"/trainingData.txt","w")

    for rule in grammar.publicRules:
        expansions = processor.processRHS(rule.rhs)
        for expansion in expansions:
            trainingFile.write(expansion+"\n")
    
