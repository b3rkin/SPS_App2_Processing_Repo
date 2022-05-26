from cgi import test
import glob
import os
from Util.Processing_func import *

parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

cell_number = 15 # Number of cellss that are used in the model

format = False
pmfcreate = True
addMissing = True

pmf_dir = os.path.join(parentDirectory,"","Processing/MACpmf")

if format:
    # Format the training data by removing [] and adding missing commas.
    for i in range(1,cell_number+1):
        dir = os.path.join(parentDirectory, "GatherData_Bayes", "Friday2_dir", "saved_data_cell" + str(i) + "_Friday_All.txt")
        cleanup_csv(dir)
        format_txt(dir)

# Empty the directory where the pmfs will be stored
if (len(os.listdir(pmf_dir))!=0):
    files = glob.glob(pmf_dir + '/*')
    for f in files:
        os.remove(f)

if pmfcreate:
    # Create the pmfs for each MAC address and insert into the model/ directory

    for i in range(1,cell_number+1):
        dir = os.path.join(parentDirectory, "Processing/raw_data/all_training_data", "saved_data_cell" + str(i) + "_totall.txt")
        create_pmf(dir,i)
    

if addMissing:
    # Clean the model files by deleting [] and "" and add missing cells to the radar maps
    files = glob.glob(pmf_dir + '/*')
    for f in files:
        add_missing_cells(f, cell_number) # This function must come before cleanup_csv
        cleanup_csv(f)  