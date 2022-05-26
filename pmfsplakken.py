import numpy as np
import pandas as pd
from IPython.display import display
import os, re
import numpy as np

data_dir = "MACpmf/"

# function to get unique values
def unique(list1):
    x = np.array(list1)
    x = np.unique(x)
    return np.ndarray.tolist(x)
      

# Get all file names minus the last 2 mac characters to get distinct mac addresses.
distinct_ap_list = [file_name[0:-5] for file_name in os.listdir(data_dir)]

distinct_ap_list = unique(distinct_ap_list)
flag = 1
counter = 0

for idx, d_ap in enumerate(distinct_ap_list):
    for file in os.listdir(data_dir):
        if re.match(d_ap, file):
            print(d_ap,file)
            if(flag == 1):
                df1 = pd.read_csv(data_dir + file, header=None)
                flag = 0
                counter += 1
            else:
                df2 = pd.read_csv(data_dir + file, header = None)     
                for i in range(df1.shape[0]): #iterate over rows
                    for j in range(1,df1.shape[1]): #iterate over columns
                        df1.iloc[i,j] += df2.iloc[i, j] #get cell value
                counter += 1
    for i in range(df1.shape[0]): #iterate over rows
        for j in range(1,df1.shape[1]): #iterate over columns
            df1.iloc[i,j] += (df1.iloc[i, j]/counter)#get cell value       
    counter = 0
    df1.to_csv('newpmfs/'+d_ap+'.csv', index=False, header= None)
    flag = 1
                
