import pandas as pd
import os
import matplotlib

currentDirectory = os.getcwd()
filePath = os.path.join(currentDirectory,"MACpmf", "00_31_92_60_ee_24.csv")
pmfCell = pd.read_csv(filePath, header = None)
print(pmfCell.iloc[[0]])

pmfCell.plot.hist(bins = 100, alpha=0.5)