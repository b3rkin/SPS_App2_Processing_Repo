from cgi import test
import pandas as pd
import os
from os.path import exists
from Util.Processing_func import cleanup_csv
from IPython.display import display
from distutils.dir_util import copy_tree
import glob

def filterMultipleMACs(data_dir):
    """This function takes a test measurement file and filters out the common mac addresses (based on last character difference)"""
    for path in os.listdir(data_dir):

        testPoint = pd.read_csv(data_dir+ '/'+ path, names = ["MAC","Rssi"],index_col=False)

        for i in range(testPoint.shape[0]): #iterate over rows
            testPoint.iloc[i,0] = testPoint.iloc[i,0][0:-1] #get cell value

        testPoint.drop_duplicates(subset ="MAC", keep = 'first', inplace = True)

        testPoint = testPoint.reset_index(drop = True)  # make sure indexes pair with number of rows

        testPoint.to_csv(data_dir + '/'+path, index=False,header= None)

def sortMeasurement(dataFile):
    """Sorts the obtained test values and returns it in a pandas dataframe"""

    testPoint = pd.read_csv(path, names = ["MAC","Rssi"])
    sortTestPoint = testPoint.sort_values(by = "Rssi", ascending = False)
    resetIndex = sortTestPoint.reset_index(drop=True) 
    return resetIndex

def calc_posterior(sortedTestPoint, prior):
    """Calculates the posterior """

    # Search until the MAC address can be found in the files and the sum is not zero
    flag = 0

    while (flag==0):

        flag = 1

        # Select the strongest MAC and corresponding signal
        StrongestMAC = sortedTestPoint.loc[0,"MAC"]
        StrongestSignal = sortedTestPoint.loc[0,"Rssi"]
        # increment for new index  
        

        # Define the posterior
        posterior   = [0. for i in range(int(cell_number))]

        # Get the file of the corresponding MAC 
        file_name_MAC = "MACpmf/" + StrongestMAC.replace(":","_") + ".csv"

        #If the file exists use it to update the prior, otherwise look at the next strongest signal map
        if(exists(file_name_MAC)): 
            df = pd.read_csv(file_name_MAC, header = None) # Read the cell data into a df

            RSS_column = df[-StrongestSignal].tolist() 
        
            # Calculate posterior
            for index in range(cell_number):
                posterior[index] = prior[index]*RSS_column[index]    

            # Normalize posterior
            sum = 0     
            for j in range(len(posterior)):    
                sum = sum + posterior[j]  

            # Search for new MAC 
            if sum == 0: 
                flag = 0
                print("sum = 0")           
            else:
                for j in range(len(posterior)):    
                    posterior[j] = posterior[j]/sum
            
            sortedTestPoint.drop(index=sortedTestPoint.index[0], axis=0, inplace=True)
            sortedTestPoint = sortedTestPoint.reset_index(drop=True)

        else:
            print("MAC is not present please try second best signal here is the MAC", file_name_MAC)
            sortedTestPoint.drop(index=sortedTestPoint.index[0], axis=0, inplace=True)
            sortedTestPoint = sortedTestPoint.reset_index(drop=True)
            flag = 0

    return posterior
  
# Set global points 
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
day = "Friday"
date = "may20"
# dirList = ["random1", "random2", "random3", "random4", "random5"]
dirList = ["South", "East", "North", "West"]
cell_number = 15
good = []
almost1 = []
almost2 = []

# Copy the test data into the working directory, change the first parameter to use other test data
copy_tree("raw_data/raw_test_data_" + date, "temporary_test_data_for_algorithm")
filterMultipleMACs("temporary_test_data_for_algorithm") # get rid of multiple mac of same access point

number_of_macs_we_want_to_iterate = 10
posterior_output = [0 for i in range(int(cell_number))]
initial_belief = [1./cell_number for i in range(int(cell_number))]
posterior = initial_belief
for i in range(1,cell_number+1):

    for macNum in range(number_of_macs_we_want_to_iterate):
        for dir in dirList:
            # Get the file and create a proper csv file of it
            path = os.path.join(parentDirectory, "Processing/temporary_test_data_for_algorithm" , "saved_data_celltest" + str(i) + "_" + day + "_" + dir + ".txt")
            cleanup_csv(path)
            sortTest = sortMeasurement(path)

            if dir == dirList[0]: # first measurement for a cell
                posterior = calc_posterior(sortTest, posterior)
            else:
                posterior = calc_posterior(sortTest, posterior)

            # Save new test point into temporary file
            sortTest.to_csv(path, index=False,header= None)
            
            # print(f' real cell = {i} and predicted cell = {posterior.index(max(posterior))+1}')

        # if macNum == 0:
        #     for index in range(len(posterior_output)):
        #         posterior_output[index] += posterior[index]*0.5
        # if macNum == 1:
        #     for index in range(len(posterior_output)):
        #         posterior_output[index] += posterior[index]*0.2
        # if macNum == 2:
        #     for index in range(len(posterior_output)):
        #         posterior_output[index] += posterior[index]*0.1
        # if macNum == 3:
        #     for index in range(len(posterior_output)):
        #         posterior_output[index] += posterior[index]*0.1
        # if macNum == 4:
        #     for index in range(len(posterior_output)):
        #         posterior_output[index] += posterior[index]*0.1
    
    posterior_output = posterior
    print(posterior_output)
    if i == posterior_output.index(max(posterior_output))+1:
        good.append(i)
    if i == posterior_output.index(max(posterior_output)) or i == posterior_output.index(max(posterior_output)) + 2:
        almost1.append(i)
    if i == posterior_output.index(max(posterior_output)) -1 or i == posterior_output.index(max(posterior_output)) + 3:
        almost2.append(i)
    posterior = initial_belief

print(day)
print("good",good)
print("almost1", almost1)
print("almost2", almost2)

# Clean the temporary files
# # Empty the directory where the pmfs will be stored
temp_dir = "temporary_test_data_for_algorithm"
if (len(os.listdir(temp_dir))!=0):
    files = glob.glob(temp_dir + '/*')
    for f in files:
        os.remove(f) 