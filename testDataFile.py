#TestDataFile

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import filedialog as fd

def main():
    #Load a whole file
    
    fileName = fd.askopenfilename()

    print("Loading...")

    dataFrame = pd.read_csv(fileName)

    print("Done!")

    time=dataFrame["Time (s)"]
    print(time)

    velocity=dataFrame["Velocity"]
    print(velocity)

    fig,ax=plt.subplots()
    ax.plot(time,velocity)

    ax.grid()
    plt.show()

def main2():
    #Load certain columns of a file

    fileName=fd.askopenfilename()

    print("Loading...")
    cols=["U-V","V-W","W-U"]
    dataFrame = pd.read_csv(fileName, usecols=cols,index_col=False)

    print("Done!")

    uv=dataFrame[cols[0]]
    vw=dataFrame[cols[1]]
    wu=dataFrame[cols[2]]

    x=[]
    for i in range(1,len(uv)+1):
        x.append(i)


    fig,ax=plt.subplots()
    ax.plot(x,uv,label=cols[0])
    ax.plot(x,vw,"r",label=cols[1])
    ax.plot(x,vw,"k",label=cols[2])

    ax.set(xlabel="Index",ylabel="Units?")

    ax.grid()
    ax.legend()
    plt.show()

def main3():
    #Load multiple files, combine data, and plot

    #Load files
    fileNames=fd.askopenfilenames()

    #Data that I want to plot
    cols=["Time (s)","TC16 - DUT1 Stator","TC17 - DUT2 Stator","DUT Raw Velocity (RPM)"]
    
    dataList=[]
    for name in fileNames:
        print("Loading new file: "+name)
        data=pd.read_csv(name,usecols=cols,index_col=False)
        dataList.append(data)

    finalFrame=pd.concat(dataList,ignore_index=True)

    time=finalFrame[cols[0]]
    temp1=finalFrame[cols[1]]
    temp2=finalFrame[cols[2]]
    speeds=finalFrame[cols[3]]

    #I cant figure it out so heres another for loop
    x=[]
    for i in range(1,len(temp1)+1):
        x.append(i)

    fig,axs=plt.subplots(2)
    axs[0].plot(x,temp1,label=cols[1])
    axs[0].plot(x,temp2,label=cols[2])
    
    axs[1].plot(x,speeds,label=cols[3])

    axs[0].set(xlabel="Index",ylabel="Temp (C)")
    axs[1].set(xlabel="Index",ylabel="Speed (RPM)")

    axs[0].grid()
    axs[0].legend()
    axs[1].grid()
    axs[1].legend()
    plt.show()

main2()
    
