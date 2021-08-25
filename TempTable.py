import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

#Load function will take csv files as input and return a pandas dataframe
def loadFunction():
    #Load one file
    #fileNames=fd.askopenfilename()
    
    #Load Multiple files
    #It can load multiple files or just a single file
    fileNames=fd.askopenfilenames()

    #Data columns to be plotted
    #Name must be EXACTLY as column in excel.csv file
    #Anyway to streamline this?
    cols=["Time (s)","TC16 - DUT1 Stator","TC17 - DUT2 Stator"]

    #for loop load the data
    #improve load order somehow?
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

    #Catch no user input?
    
    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True)

    return finalFrame,cols


def main():
    dataFrame,cols=loadFunction()

    temp1=list(dataFrame[cols[1]])
    temp2=list(dataFrame[cols[2]])
    
    #Create an index to plot with
    iList=[]
    for i in range(1,len(temp1)+1):
        iList.append(i)
        
    #Find Maximum of subset 1
    #subset 1 goes from index 0 to 152000
    #DUT1
    d1sub1=temp1[0:152000]
    d1max1=max(d1sub1)
    d1in1=d1sub1.index(d1max1)

    #DUT2
    d2sub1=temp2[0:152000]
    d2max1=max(d2sub1)
    d2in1=d2sub1.index(d2max1)
    
    #Find average of subset 1
    #DUT1
    d1sub12=temp1[d1in1:152000]
    d1avg1=sum(d1sub12)/len(d1sub12)

    #DUT2
    d2sub12=temp2[d2in1:152000]
    d2avg1=sum(d2sub12)/len(d2sub12)
    
    #Find Maximum of subset 2
    #subset 2 goes from index 220100 to 363300
    #DUT1
    d1sub2=temp1[220100:363300]
    d1max2=max(d1sub2)
    d1in2=d1sub2.index(d1max2)+220100

    #DUT2
    d2sub2=temp2[220100:363300]
    d2max2=max(d2sub2)
    d2in2=d2sub2.index(d2max2)+220100
    
    #Find average of subset 2
    #DUT1
    d1sub22=temp1[d1in2:363300]
    d1avg2=sum(d1sub22)/len(d1sub22)

    #DUT2
    d2sub22=temp2[d2in2:363300]
    d2avg2=sum(d2sub22)/len(d2sub22)

    #Graph Data
    fig,ax=plt.subplots()
    ax.plot(iList,temp1,"r",label=cols[1])
    ax.plot(iList,temp2,"b",label=cols[2])
    #Plot maximum marker
    #ax.plot(iList[d1in1],d1max1,"*k",label="D1 - MaxTemp 1")
    #ax.plot(iList[d1in2],d1max2,"*k",label="D1 - MaxTemp 2")

    #ax.plot(iList[d2in1],d2max1,"ok",label="D2 - MaxTemp 1")
    #ax.plot(iList[d2in2],d2max2,"ok",label="D2 - MaxTemp 2")

    #Create a dataframe, upload into CSV
    DUT1Max=d1max2-d1max1
    DUT1Avg=d1avg2-d1avg1

    DUT2Max=d2max2-d2max1
    DUT2Avg=d2avg2-d2avg1
    
    DUT1MAX=[DUT1Max]
    DUT1AVG=[DUT1Avg]
    DUT2MAX=[DUT2Max]
    DUT2AVG=[DUT2Avg]
    dic={"DUT 1 - dMax Temp": DUT1MAX,
         "DUT 1 - dAvg Temp": DUT1AVG,
         "DUT 2 - dMax Temp": DUT2MAX,
         "DUT 2 - dAvg Temp": DUT2AVG}
    
    finalFrame=pd.DataFrame(data=dic)

    #Display Table
    print(finalFrame)


    #Display Graph
    ax.grid()
    ax.legend()
    ax.set_ylabel("Temperature (deg C)")
    ax.set_xlabel("Data Point Number (Index)")
    ax.set_title("Temperature of DUTs 1 and 2")
    plt.show()


main()
