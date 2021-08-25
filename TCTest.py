import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

#Load function will take csv files as input and return a pandas dataframe
def loadFunction():
    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #Data columns to be plotted
    cols=["TC5 - DUT1 - 1st Therm PLE",
          "TC6 - DUT1 - Middle Therm PLE",
          "TC7 - DUT1 - 2nd Therm PLE",
          "TC13 - DUT2 - 1st Therm PLE",
          "TC14 - DUT2 - Middle Therm PLE",
          "TC15 - DUT2 - 2nd Therm PLE",
          "TC16 - DUT1 Stator",
          "TC17 - DUT2 Stator"]

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
    newFrame,cols=loadFunction()

    #Overall Temps
    #DUT1 TCs
    fig1,ax1=plt.subplots()
    #DUT1 Differences
    fig3,ax3=plt.subplots()

    tcs1=["TC5 - DUT1 - 1st Therm PLE",
          "TC6 - DUT1 - Middle Therm PLE",
          "TC7 - DUT1 - 2nd Therm PLE",
          "TC16 - DUT1 Stator"]

    for tc in tcs1:
        ax1.plot(newFrame[tc],label=tc)

        if(tc != "TC16 - DUT1 Stator"):
            diff=newFrame["TC16 - DUT1 Stator"].subtract(newFrame[tc])
            diff=list(diff)
            ax3.plot(diff,label=tc)

    ax1.grid()
    ax1.legend()
    ax1.set_title("Thermocouples on DUT1")
    ax1.set_xlabel("Data Point Number (Index)")
    ax1.set_ylabel("Temperature (deg C)")
    ax1.set_ylim(100,200)

    ax3.grid()
    ax3.legend()
    ax3.set_title("Thermocouple Differences on DUT1 (DUT1 - TC)")
    ax3.set_xlabel("Data Point Number (Index)")
    ax3.set_ylabel("Temperature (deg C)")

    #DUT2 TCs
    fig2,ax2=plt.subplots()

    #DUT2 Differences
    fig4,ax4=plt.subplots()

    tcs2=["TC13 - DUT2 - 1st Therm PLE",
          "TC14 - DUT2 - Middle Therm PLE",
          "TC15 - DUT2 - 2nd Therm PLE",
          "TC17 - DUT2 Stator"]
    
    for tc in tcs2:
        temp=newFrame[tc]
        ax2.plot(temp,label=tc)

        if(tc != "TC17 - DUT2 Stator"):
            diff2=newFrame["TC17 - DUT2 Stator"].subtract(newFrame[tc])
            diff2=list(diff2)
            ax4.plot(diff2,label=tc)

    ax2.grid()
    ax2.legend()
    ax2.set_title("Thermocouples on DUT2")
    ax2.set_xlabel("Data Point Number (Index)")
    ax2.set_ylabel("Temperature (deg C)")
    ax2.set_ylim(100,200)

    ax4.grid()
    ax4.legend()
    ax4.set_title("Thermocouple Differences on DUT2 (DUT2 - TC)")
    ax4.set_xlabel("Data Point Number (Index)")
    ax4.set_ylabel("Temperature (deg C)")

    plt.show()

main()