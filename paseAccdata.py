from re import L
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

sample_size = 1

def smoothArray(values, smoothing):
    value = values.iloc[0]

    for i in range(values.size):
        currentValue = values.iloc[i]
        value += (currentValue-value)/smoothing
        values.iloc[i] = value

def windowSearch(points,steps, deltaUp, deltaDown,windowLength):
    up = False
    down = False
    
    idxList = [x for x in range(windowLength)]

    for i in range(len(points)):
        # print("i",i)
        idxList.remove(i)
        for idx in idxList:
            delta = points[i] - points[idx]

            if delta >= deltaUp:
                up = True
            elif delta <= deltaDown:
                down = True
            
            if up and down:
                steps = steps + 1
                up = False
                down = False
                return steps
        idxList.append(i)
        
    return steps

def walkThroughData(data,windowLength):
    """Walks through column using a window of certain amount of points"""
    steps = 0
    for i in range(0,len(data)-windowLength,windowLength):
        window = np.array(data[i:i+windowLength])
        steps = windowSearch(window,steps,-1.5,1.5,windowLength)

    return steps


file_names = ["saved_dataACC_B20.txt","saved_dataACC_B15.txt","saved_dataACC_B15_2.txt","saved_dataACC_B20_2.txt","saved_dataACC_B20_3.txt"] #,"saved_dataACC_B15_2.txt"]
# Remove all square brackets

for i in range(len(file_names)):
    with open(file_names[i], 'r') as my_file:
        text = my_file.read()
        text = text.replace("[", "")
        text = text.replace("]", ",")
    with open(file_names[i], 'w') as my_file:
        my_file.write(text)


    df = pd.read_csv(file_names[i])
    df = df.iloc[: , :-1]

    dfz = df["z"]
    print(f'{file_names[i]} not smooth 5 {walkThroughData(dfz,5)}')   
    print(f'{file_names[i]} not smooth 6 {walkThroughData(dfz,6)}')   
    print(f'{file_names[i]} not smooth 7 {walkThroughData(dfz,7)}')   
    print(f'{file_names[i]} not smooth 8 {walkThroughData(dfz,8)}')   
    print(f'{file_names[i]} not smooth 9 {walkThroughData(dfz,9)}')   
    print(f'{file_names[i]} not smooth 10 {walkThroughData(dfz,10)}')   
    print(f'{file_names[i]} not smooth 11 {walkThroughData(dfz,11)}')   
    print(f'{file_names[i]} not smooth 12 {walkThroughData(dfz,12)}')   
    
    smoothArray(dfz,2)
    print(f'{file_names[i]} smooth 5 {walkThroughData(dfz,5)}')   
    print(f'{file_names[i]} smooth 6 {walkThroughData(dfz,6)}')   
    print(f'{file_names[i]} smooth 7 {walkThroughData(dfz,7)}')   
    print(f'{file_names[i]} smooth 8 {walkThroughData(dfz,8)}')   
    print(f'{file_names[i]} smooth 9 {walkThroughData(dfz,9)}')   
    print(f'{file_names[i]} smooth 10 {walkThroughData(dfz,10)}')   
    print(f'{file_names[i]} smooth 11 {walkThroughData(dfz,11)}')   
    print(f'{file_names[i]} smooth 12 {walkThroughData(dfz,12)}')   




   
