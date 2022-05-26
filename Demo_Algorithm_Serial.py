from cgi import test
import pandas as pd
import os
from os.path import exists
from Util.Processing_func import cleanup_csv
from IPython.display import display
from distutils.dir_util import copy_tree
import glob

def filterMultipleMACs(data_dir):
    """This function takes a test measurement file and filters out the common mac addresses (based on last character difference). Cleanup is also
    done in this function"""
    for path in os.listdir(data_dir): # Go trough all test files

        testPoint = pd.read_csv(data_dir+ '/'+ path, names = ["MAC","Rssi"],index_col=False) # get test file into df
        # discard the last character of the MAC addresses
        for i in range(testPoint.shape[0]): #iterate over rows
            testPoint.iloc[i,0] = testPoint.iloc[i,0][0:-1] #get cell value
        # Drop the duplicate MAC addresses and keep the strongest one
        testPoint.drop_duplicates(subset ="MAC", keep = 'first', inplace = True)
        testPoint = testPoint.reset_index(drop = True)  # make sure indexes pair with number of rows
        # Save the test measurement in the same place
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
  
# Set testing variables
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
days = ['Friday', 'Wednesday']
day = days[1]
date = "may25-2"
# dirList = ["random1", "random2", "random3", "random4", "random5"][:]
# dirList = ["South", "East", "North", "West"]
dirList = ["East_1","East_2","East_3"][:]
# dirList = ["West_1","West_2","West_3"][:-1]
# dirList = ["North_1","North_2","North_3"][:-1]
# dirList = ["South_1","South_2","South_3"][:-1]
cell_number = 15
# Initialize arrays to hold test results
good = []
almost1 = []
almost2 = []
wrong = []

# Copy the test data into the working directory, and format the testing data to fit the algorithm
temp_test_path = "temporary_test_data_for_algorithm"
copy_tree("raw_data/raw_test_data_" + date, temp_test_path)
# for test_file in os.listdir(temp_test_path):
#     cleanup_csv(temp_test_path+'/'+test_file)
# Filter the multiple macs in all testing data files
filterMultipleMACs("temporary_test_data_for_algorithm") # get rid of multiple mac of same access point

number_of_macs_we_want_to_iterate = 1

initial_belief = [1./cell_number for i in range(int(cell_number))]
posterior = initial_belief  # The posterior list will be used initially as initial belief, 
                            # and both prior and posterior throughout the calculations

# Iterate through all test points for each cell
for i in range(1,cell_number+1):
    for dir in dirList:
        # Iterate through all MACs in a single measurement (The calculations are done in parallel)
        for macNum in range(number_of_macs_we_want_to_iterate):

            # Get the file and create an ordered data frame
            path = os.path.join(parentDirectory, "Processing/temporary_test_data_for_algorithm" , \
                "saved_data_celltest" + str(i) + "_" + day + "_" + dir + ".txt")
            sortTest = sortMeasurement(path)
            # Calculate the posterior based on the prior, which is the previous posterior.
            posterior = calc_posterior(sortTest, posterior)
            # Save new test point (with used mac deleted) into temporary file
            sortTest.to_csv(path, index=False,header= None)
            # Print the intermediate prediction
            print(f' real cell = {i} and predicted cell = {posterior.index(max(posterior))+1}')

    # Put the prediction result in the corresponding array
    prediction = posterior.index(max(posterior))
    if i == prediction+1:
        good.append(i)
    elif i == prediction or i == prediction + 2:
        almost1.append(i)
    elif i == prediction -1 or i == prediction + 3:
        almost2.append(i)
    else:
        wrong.append(i)
    # Reset the posterior to initial belief for the calculations of a new cell
    posterior = initial_belief

# Print the testing results
print(day, date)
print("#: ",len(good),", good:    ",good)
print("#: ",len(almost1),", almost-1:", almost1)
print("#: ",len(almost2),", almost-2:", almost2)
print("#: ",len(wrong), ", wrong:   ", wrong)

# Clean the temporary files
# # Empty the directory where the pmfs will be stored
temp_dir = "temporary_test_data_for_algorithm"
if (len(os.listdir(temp_dir))!=0):
    files = glob.glob(temp_dir + '/*')
    for f in files:
        os.remove(f) 