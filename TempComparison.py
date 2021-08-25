from logging import PlaceHolder
from matplotlib.colors import hexColorPattern
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

def loadFunction(type,sheets):
    #Load one file
    fileName=fd.askopenfilenames()

    if(type == 1209):
        skipRows=[2]
        head=1
    elif(type == 1229):
        skipRows=[1]
        head=0

    #for loop load the data
    loadTime=0
    
    for name in fileName:
        print("Loading new file: "+name)
        t0=t.time()
        data=pd.read_excel(name,sheet_name=sheets,header=head,skiprows=skipRows,index_col=False)
        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
    print("Finished loading files, total load time: "+str(round(loadTime,3))+" seconds")
    
    finalFrame=data

    #Return dataframe and used columns
    return finalFrame

#Clean Data of anything other than floats and ints
def cleanData(data):
    #Clean out strings
    for i in range(len(data)-1):
        if(type(data[i]) == str):
            data.pop(i)
    #Fix weird NaN problem in 500 RPM
    data.fillna(0,inplace=True)
    #Clean 
    return data

def main():
    #Load Data from excel sheets
    sheets=["500 RPM",
            "1000 RPM",
            "2000 RPM",
            "3000 RPM",
            "4000 RPM",
            "5000 RPM",
            "6000 RPM"]

    print("Load file (F125-1209)")
    onineFrame=loadFunction(1209,sheets)

    print("Load file (F125-1229)")
    twonineFrame=loadFunction(1229,sheets)

    #Get Data from dataframe
    
    tcs=["Stator End Turn Rear 6  O'clock (TC3-98-WELD)",
         "Stator End Turn Front 6  O'clock  (TC7-98-CROWN)",
         "Stator Face Rear 6 O'clock  (TC11-98-WL)",
         "Stator Face Front 6 O'clock  (TC15-98-CL)"]
    #Of course the names of the columns don't match
    oldtcs=["TC3","TC7","TC11","TC15"]

    #idk what to call it so its plist now
    plist=[]
    for sheet in sheets:
        #Figures to show the temperatures of OIL and WEG TCs
        fig=plt.figure(figsize=(16.0,10.0))
        ax=fig.add_subplot()

        #Figures for calculating difference between TCs
        dfig=plt.figure(figsize=(16.0,10.0))
        ax2=dfig.add_subplot()

        avgTC=[]
        avgTC.append(sheet)
        #TeHermoCOUPle
        #for tc in tcs:
        for i in range(len(tcs)):
            #Get Data
            oldtemp=onineFrame[sheet][oldtcs[i]]
            newtemp=twonineFrame[sheet][tcs[i]]
        
            #Clean data
            oldtemp=list(cleanData(oldtemp))
            newtemp=list(cleanData(newtemp))

            #Create Difference
            difference=[]
            j=0
            while j<len(oldtemp) and j<len(newtemp):
                difference.append(oldtemp[j]-newtemp[j])
                j+=1

            #Plot data
            ax.plot(oldtemp,label=oldtcs[i])
            ax.plot(newtemp,"--",label=tcs[i])
            ax.set_title(sheet)
            ax.grid(color="grey")
            ax.legend()

            ax2.plot(difference,label=tcs[i])
            ax2.set_title("TC Difference (1229 - 1209) - "+sheet)
            ax2.grid(color="grey")
            ax2.legend()

            #Extra Data
            avg=np.average(difference)
            avgTC.append(avg)
            #print(sheet+" - "+tc+" - AVG Diff.: "+str(round(avg,3)))

            #Save a copy
            #plt.savefig(sheet+".png")
        
        plist.append(avgTC)
    
    avgDF=pd.DataFrame(plist,columns=["Speed (RPM)",
                                      "Stator End Turn Rear 6  O'clock (TC3-98-WELD)",
                                      "Stator End Turn Front 6  O'clock  (TC7-98-CROWN)",
                                      "Stator Face Rear 6 O'clock  (TC11-98-WL)",
                                      "Stator Face Front 6 O'clock  (TC15-98-CL)"])

    #fig3,ax3=plt.subplots()
    ax3=avgDF.plot(x="Speed (RPM)",kind="bar",stacked=False)
    ax3.grid("grey")
    ax3.set_title("Avg. Temperature Difference (1209-1229) of Thermocouples")
    ax3.set_ylabel("Temperature (deg C)")
    ax3.legend()

    plt.show()

main()