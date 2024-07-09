#This program reorganizes the bulk question JSON
#from questions-and-answers to question-with-all answers
#if that makes sense
import sys
import json

jsonFilePath = sys.argv[1]
outfileName = sys.argv[2]
jsonFile = open(jsonFilePath, "r")
j = json.load(jsonFile)
jsonFile.close()


#This program runs under the assumption that all similar questions are grouped together
currentIndex = 0
masterList = []
while currentIndex < len(j):
    newEntry = {"output":j[currentIndex]["output"]}
    questions = [j[currentIndex]["instruction"]]
    currentIndex += 1
    while (currentIndex < len(j) and j[currentIndex]["output"] == newEntry["output"]):
        questions.append(j[currentIndex]["instruction"])
        currentIndex += 1
    newEntry["questions"] = questions
    masterList.append(newEntry)

outfile = open(outfileName, "w")
json.dump(masterList, outfile, indent = 2)
outfile.close()

