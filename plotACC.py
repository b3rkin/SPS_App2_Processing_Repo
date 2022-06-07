import pandas as pd
import matplotlib.pyplot as plt

# file_names = ["saved_dataACC_B20.txt","saved_dataACC_B15.txt","saved_dataACC_B15_2.txt","saved_dataACC_B20_2.txt","saved_dataACC_B20_3.txt" ,
file_names = ["saved_dataACC_M16.txt","saved_dataACC_M15N_4E.txt","saved_dataACC_M15W_4ishE.txt"]#"saved_dataACC_B15_4.txt","saved_dataACC_B15_555.txt","saved_dataACC_B15_105.txt"]

for i in range(len(file_names)):
    df = pd.read_csv("ACCdata/" + file_names[i])
    df = df.iloc[: , :-1]
    dfz = df["z"]

    dfz.plot()
    plt.show()