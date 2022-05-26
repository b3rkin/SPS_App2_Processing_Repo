# File to split the concatenated test data points to seperate measurement points
import os
from Process_func import *
import glob

currentDirectory = os.getcwd()
filePath = os.path.join(currentDirectory,"raw_data")


dirList = ["n","w","e","s"]
# dirList = ["s"]
cellNumber = 15

# empty split folder
splitPath = os.path.join(filePath,"split_test_data")
if (len(os.listdir(splitPath))!=0):
    files = glob.glob(splitPath + '/*')
    for f in files:
        os.remove(f)
    

for dir in dirList:
    for i in range(1,cellNumber+1):
        parsePath = os.path.join(filePath,"concat_test_data","testDatatest" + str(i) + "_Wednesday_" + dir + ".txt")

        with open(parsePath,'r') as file:
            lines = file.readlines()

        countBegin = 1
        countEnd = 0
        measurement = 1

        # Strips the newline character
        for line in lines:
            countEnd += 1

            if line[0] == "*" and line[1] == ",":
                if dir == "s":
                    dirsave = "South"
                if dir == "n":
                    dirsave = "North"
                if dir == "w":
                    dirsave = "West"
                if dir == "e":
                    dirsave = "East"

                savePath = os.path.join(filePath,"split_test_data","saved_data_celltest" + str(i) + "_Wednesday_" + dirsave + "_" + str(measurement) + ".txt")
                with open(savePath,"w") as save:
                    save.writelines(lines[countBegin:countEnd-1])
                cleanup_csv(savePath)
                measurement += 1
                countBegin = countEnd
                if measurement == 4:
                    break
                
