#MultiFileProcess

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
          "DUT Raw Velocity (RPM)",
          "DUT Calculated Torque (Nm)",
          "ICM2 - Active Fault",
          "ICM2 - Active Warning",
          "LMCM - Id (A)",
          "LMCM - Iq (A)"]

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

    time=finalFrame[cols[0]]
    temp1=finalFrame[cols[1]]
    temp2=finalFrame[cols[2]]
    speeds=finalFrame[cols[3]]
    torque=finalFrame[cols[4]]
    fault=list(finalFrame[cols[5]])
    warning=list(finalFrame[cols[6]])
    
    iD=finalFrame[cols[7]]
    iQ=finalFrame[cols[8]]

    #Get where fault codes started
    indexW=warning.index(1)
    indexF=fault.index(1)

    #Create multiple axes, 0 -> temp graph, 1 -> Velocity graph, 2 -> Torque
    fig,axs=plt.subplots(3)
    axs[0].plot(time,temp1,label=cols[1])
    axs[0].plot(time,temp2,color="green",label=cols[2])
    axs[1].plot(time,speeds,label=cols[3])
    axs[2].plot(time,torque,label=cols[4])
    

    axs[0].set(ylabel="Temp (C)")
    axs[1].set(ylabel="Speed (RPM)")
    axs[2].set(xlabel="Time (Seconds)",ylabel="Torque (Nm)")

    #Create Another figure with multiple axes, 0 -> iq, 1-> id
    fig2,axs2=plt.subplots(2)
    
    axs2[0].plot(time,iD,label=cols[7])
    axs2[1].plot(time,iQ,label=cols[8])

    
    #Add warning/fault index
    for ax in axs2:
        ax.axvline(time[indexW],0,1,color="orange")
        ax.axvline(time[indexF],0,1,color="red")
        
        ax.grid()
        ax.legend()

    #Add warning/fault index
    for ax in axs:
        ax.axvline(time[indexW],0,1,color="orange")
        ax.axvline(time[indexF],0,1,color="red")
        
        ax.grid()
        ax.legend()

    axs2[0].set(ylabel="Current (A)")
    axs2[1].set(xlabel="Time (Seconds)",ylabel="Current (A)")
    
    
    plt.show()

main()
