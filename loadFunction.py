import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

#Load function will take csv files as input and return a pandas dataframe
def loadFunction():
    
    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #Data columns to be plotted
    cols=["Time (s)",
          "TC16 - DUT1 Stator",
          "TC17 - DUT2 Stator",
          "DUT Raw Velocity (RPM)"]

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
