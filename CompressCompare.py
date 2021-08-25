#Written by Nathan Dodson
import os
import time as t
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd




#Load function integrated into main for ease of use
def main():
    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #for loop load the data
    loadTime=0
    uncompSizes=[]
    compSizes=[]
    for name in fileNames:
        
        print("Loading new file: "+name)
        #Load a file, create dataframe
        t0=t.time()
        data=pd.read_csv(name,index_col=False)

        #Trim the data
        data=trim(data)
        
        #Load trimmed dataframe to csv
        compress(data,name)

        #Take time stamp, finish file
        print("File Done!")
        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
        print("It took "+str(round(deltaT,3))+" seconds to process this file.")

        #Get file sizes
        uncompStats=os.stat(name)
        compStats=os.stat(name+".zip")

        #Convert bytes to MB
        uncompSize=round(uncompStats[6]/1000000,3)
        compSize=round(compStats[6]/1000000,3)

        uncompSizes.append(uncompSize)
        compSizes.append(compSize)

    print("Finished loading and trimming files, total time: "+str(round(loadTime,3))+" seconds.")
    
    fig1,ax1=plt.subplots()
    ax1.set(xlabel="File Number",ylabel="File Size (MB)")

    plt.plot(uncompSizes,"r",label="Original File Size")
    plt.plot(compSizes,"b",label="Trimmed and Compressed File Size")

    ax1.grid()
    ax1.legend()
    plt.show()

#Function will check and trim a dataframe of columns with all zeros, returns trimmed dataframe
def trim(dataFrame):
    
    #Check columns
    print("Checking...")
    cols=dataFrame.columns
    toDel=[]
    
    for col in cols:
        if(np.count_nonzero(dataFrame[col])==0):
            toDel.append(col)
                
    #Trim dataframe
    print("Trimming...")
    TdataFrame = dataFrame.drop(columns=toDel)

    return TdataFrame

#Function will create a compressed .csv of input dataframe  
def compress(dataFrame,name):
    
    print("Compressing...")
    trimmedName=name.split("/")
    compressOptions = dict(method='zip',archive_name=trimmedName[len(trimmedName)-1]) 
    dataFrame.to_csv(name+'.zip', index=False,compression=compressOptions)
    

main()
