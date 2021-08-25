import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

#Load function will take csv files as input and return a pandas dataframe
def loadFunction():
    #Load one file
    #fileNames=fd.askopenfilenames()
    
    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #Data columns to be plotted
    cols=["TC3 - DUT1 - 129 MS",
          "TC4 - DUT1 - 129 PLE",
          "TC5 - DUT1 - 1st Therm PLE",
          "TC6 - DUT1 - Middle Therm PLE",
          "TC7 - DUT1 - 2nd Therm PLE",
          "TC11 - DUT2 - 129 MS",
          "TC12 - DUT2 - 129 PLE",
          "TC13 - DUT2 - 1st Therm PLE",
          "TC14 - DUT2 - Middle Therm PLE",
          "TC15 - DUT2 - 2nd Therm PLE",]

    #for loop load the data
    dataList=[]
    loadTime=0
    for name in fileNames:
        print("Loading new file: "+name)
        t0=t.time()
        data=pd.read_csv(name,usecols=cols,index_col=False)
        dataList.append(data)
        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
    print("Finished loading files, total load time: "+str(round(loadTime,3))+" seconds")
    
    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True)

    #Return dataframe and used columns
    return finalFrame,cols

def main():
    finalFrame,cols=loadFunction()

    fig,ax=plt.subplots()
    fig2,ax2=plt.subplots()

    for i in range(len(cols)):
        if(i<=4):
            ax.plot(finalFrame[cols[i]],label=cols[i])
        else:
            ax2.plot(finalFrame[cols[i]],label=cols[i])

    

    ax.grid()
    ax.legend()

    ax2.grid()
    ax2.legend()

    plt.show()

main()
