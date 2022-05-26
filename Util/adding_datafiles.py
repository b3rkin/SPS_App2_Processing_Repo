import pandas as pd
import os
import numpy as np
from os.path import exists
import csv
import glob


# Parent directory folder 
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Make a selection of the files who got double MAC addresses
duplicate = []

# Fill it up with commas
def formatCSV(DataFile):
    """This function adds commas to the first line of a csv to be able to obtain a pandas df"""
    max_commas = 0 # Max number of commmas in single line
    missing_commas = 0 # Missing commas in firts line
    first_commas = 0 # Number of commas in first line
    flag = True
    # Obtain max number of commas in any line in the file
    file = open(DataFile)
    for line in file: 
        if(flag):# Just to get number of commas in the first line
            first_commas = line.count(',')
            flag = False
        if(line.count(',') > max_commas):
            max_commas = line.count(',')
    file.close()

    missing_commas = max_commas- first_commas # Obtain missing commmas if any

    # Add the missing commas to the first line 
    flag = True
    if(missing_commas >0):
        commas = ""
        for ij in range(missing_commas): # Get number of missing commas in string
            commas += ","
        newf=""
        with open(DataFile,'r') as f:
            for line in f:
                if(flag): # Append the commas to just the first line
                    newf += line.strip()+commas+"\n"
                    flag = False
                else:
                    newf += line.strip()+"\n"
                
        with open(DataFile,'w') as f: # Write the newly formed correct file
            f.write(newf)

def cleanupCSV(file_name):
     # Format the training data
        with open(file_name, 'r') as my_file:
            text = my_file.read()
            text = text.replace("[", "")
            text = text.replace("]", "")
            text = text.replace(" ", "")
        
        with open(file_name, 'w') as my_file:
            my_file.write(text)
    
    
    # Iterate over files for each cells training data

duplic  
for i in range(1,16):
    # Select all direction files 
    pathNorth = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_North.txt")
    pathEast = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_East.txt")
    pathSouth = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_South.txt")
    pathWest = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_West.txt")

    # Read text file and get mac address as index 
    dfNorth = pd.read_csv(pathNorth, header = None)
    dfEast = pd.read_csv(pathEast, header = None)
    dfSouth = pd.read_csv(pathSouth, header = None)
    dfWest = pd.read_csv(pathWest, header = None)

    # pd.concat([dfNorth,dfEast], axis = 1)

    duplicateRowsNorth = dfNorth[dfNorth.duplicated([0])]
    if not duplicateRowsNorth.empty:
        duplicate.append(str(i)+"_North")

    if not dfEast[dfEast.duplicated([0])].empty:
        duplicate.append(str(i)+"_East")
    
    if not dfWest[dfWest.duplicated([0])].empty:
        duplicate.append(str(i)+"_West")
    
    if not dfSouth[dfSouth.duplicated([0])].empty:
        duplicate.append(str(i)+"_South")
    
    print(duplicate)
#     # Set mac addresses as index
    # dataframe.to_csv("saved_data_cell1_Tuesday.csv", index = "False")

# for i in range(1,16):
#     pathNorth = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_North.txt")
#     cleanupCSV(pathNorth)
#     formatCSV(pathNorth)
#     pathEast = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_East.txt")
#     cleanupCSV(pathEast)
#     formatCSV(pathEast)
#     pathSouth = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_South.txt")
#     cleanupCSV(pathSouth)
#     formatCSV(pathSouth)
#     pathWest = os.path.join(parentDirectory,"App2_data_Tuesday","saved_data_cell" + str(i) + "_Tuesday_West.txt")
#     cleanupCSV(pathWest)
#     formatCSV(pathWest)



   