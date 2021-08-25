#Written by Nathan Dodson and Carola Sague
#Script will load in as many data files as the user inputs, process the temperature data, and then spit out a table of outputs as well as a graph of the temperature data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

#Load function will take csv files as input and return a pandas dataframe
def loadFunction():
    
    #Load Multiple files
    #It can load multiple files or just a single file
    fileNames=fd.askopenfilenames()

    #Data columns to be plotted
    #Name must be EXACTLY as column in excel.csv file
    #Anyway to streamline this?
    cols=["Time (s)",
          "TC16 - DUT1 Stator",
          "TC17 - DUT2 Stator"]

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
    print("Finished loading files, total load time: "+str(round(loadTime,3))+" seconds")\
    
    #Mesh all of the dataframes from dataList together into one dataFrame
    finalFrame=pd.concat(dataList,ignore_index=True)

    return finalFrame,cols


def main():
    dataFrame,cols=loadFunction()

    #Organize Data
    temp1=list(dataFrame[cols[1]])
    temp2=list(dataFrame[cols[2]])

    #Smooth that Data!
    #Carola wrote this
    num=0
    smoothD1=[]
    while num < len(temp1):
        subset=temp1[num:num+500]
        subsetAVG=np.average(subset)
        smoothD1.append(subsetAVG)
        num=num+500
        
    num=0
    smoothD2=[]
    while num < len(temp2):
        subset=temp2[num:num+500]
        subsetAVG=np.average(subset)
        smoothD2.append(subsetAVG)
        num=num+500
        
    #Take the D1 derivative
    derivD1=list(np.gradient(smoothD1))

    #Temporary display
    dFig,dAx=plt.subplots()
    dAx.plot(derivD1,label="Deriv "+cols[1])
    dAx.set_title("Derivative of Smoothed Temperature Data")
    dAx.set_xlabel("Data Point Number (Index)")
    dAx.set_ylabel("Derivative of Temp")
    dAx.legend()
    dAx.grid()

    print("Calculating Max D1")
    #Max points D1
    maxderpointsD1=[]
    maxderpointsD1.append(0)
    index=1
    while index < len(derivD1):
        if(derivD1[index]>5 and derivD1[index-1]<derivD1[index] and derivD1[index+1]<derivD1[index]):
            maxderpointsD1.append(index)
            index=index+1
        else:
            index=index+1

    print("Calculating Min D1")  
    #Min Points D1
    minderpointsD1=[]
    index=1
    while index < len(derivD1):
        if(derivD1[index]<-5 and derivD1[index-1]>derivD1[index] and derivD1[index+1]>derivD1[index]):
            minderpointsD1.append(index)
            index=index+5
        else:
            index=index+1

    #Take the D2 derivative
    derivD2=list(np.gradient(smoothD2))

    print("Calculating Max D2")
    #Max points D2
    maxderpointsD2=[]
    index=1
    maxderpointsD2.append(0)
    while index < len(derivD2):
        if(derivD2[index]>5 and derivD2[index-1]<derivD2[index] and derivD2[index+1]<derivD2[index]):
            maxderpointsD2.append(index)
            index=index+1
        else:
            index=index+1

    print("Calculating Min D2")
    #Min Points D2
    minderpointsD2=[]
    index=1
    while index < len(derivD2):
        if(derivD2[index]<-5 and derivD2[index-1]>derivD2[index] and derivD2[index+1]>derivD2[index]):
            minderpointsD2.append(index)
            index=index+5
        else:
            index=index+1

    #Graph Smoothed Data
    fig,ax=plt.subplots()
    ax.plot(smoothD1,"r",label=cols[1])
    ax.plot(smoothD2,"b",label=cols[2])

    D1maxs=[]
    D1avgs=[]
    D2maxs=[]
    D2avgs=[]
    print("Entering the danger zone")
    for j in range(len(maxderpointsD1)):
        D1subset=[]
        D2subset=[]
        D1adjustment=0
        D2adjustment=0
        
        tempMaxD1=int(maxderpointsD1[j])
        tempMinD1=int(minderpointsD1[j])
        tempMaxD2=int(maxderpointsD2[j])
        tempMinD2=int(minderpointsD2[j])

        #Create a subset for D1
        for i in range(len(smoothD1)):
            if(i<=tempMaxD1):
                D1adjustment=i
            if(i>=tempMaxD1 and i<=tempMinD1):
                D1subset.append(smoothD1[i])
                
        #Create a subset for D2     
        for i in range(len(smoothD2)):
            if(i<=tempMaxD2):
                D2adjustment=i
            if(i>=tempMaxD2 and i<=tempMinD2):
                D2subset.append(smoothD2[i])

        #Get Maximum of D1Subset
        D1max=max(D1subset)

        #Get Maximum of D2Subset
        D2max=max(D2subset)

        #Plot Found Maximum
        D1maxXValue=D1adjustment+D1subset.index(D1max)
        ax.plot(D1maxXValue,D1max,"*k",markersize=12)

        D2maxXValue=D2adjustment+D2subset.index(D2max)
        ax.plot(D2maxXValue,D2max,"*k",markersize=12)

        #Annotate the Peak Value
        #D1
        plt.text(D1maxXValue,D1max,str(round(D1max,2)))
        #D2
        plt.text(D2maxXValue,D2max,str(round(D2max,2)))

        #Create new D1 subset for average
        D12subset=smoothD1[D1maxXValue:tempMinD1]
        #Create new D2 subset for average
        D22subset=smoothD2[D2maxXValue:tempMinD2]

        #Find the D1 Average
        D1avg=np.average(D12subset)
        #Find the D2 Average
        D2avg=np.average(D22subset)

        #Log maxs and avgs
        D1maxs.append(D1max)
        D1avgs.append(D1avg)
        D2maxs.append(D2max)
        D2avgs.append(D2avg)

        
    #Calculate Differences
    DUT1MAX=[]
    DUT1AVG=[]
    DUT2MAX=[]
    DUT2AVG=[]
    n=0
    while n < len(D1maxs):
        DUT1MAX.append(D1maxs[n+1]-D1maxs[n])
        DUT1AVG.append(D1avgs[n+1]-D1avgs[n])
        DUT2MAX.append(D2maxs[n+1]-D2maxs[n])
        DUT2AVG.append(D2avgs[n+1]-D2avgs[n])
        n=n+2
        
    #Create a dataframe, upload into CSV
    dic={"DUT 1 - dMax Temp": DUT1MAX,
         "DUT 1 - dAvg Temp": DUT1AVG,
         "DUT 2 - dMax Temp": DUT2MAX,
         "DUT 2 - dAvg Temp": DUT2AVG}
    
    finalFrame=pd.DataFrame(data=dic)
    
    #Take average of each column
    D1MaxAverage=np.average(finalFrame["DUT 1 - dMax Temp"])
    D1AvgAverage=np.average(finalFrame["DUT 1 - dAvg Temp"])
    D2MaxAverage=np.average(finalFrame["DUT 2 - dMax Temp"])
    D2AvgAverage=np.average(finalFrame["DUT 2 - dAvg Temp"])
    #Take standard deviation of each column
    D1MaxSTD=np.std(finalFrame["DUT 1 - dMax Temp"])
    D1AvgSTD=np.std(finalFrame["DUT 1 - dAvg Temp"])
    D2MaxSTD=np.std(finalFrame["DUT 2 - dMax Temp"])
    D2AvgSTD=np.std(finalFrame["DUT 2 - dAvg Temp"])
    
    newRow=pd.DataFrame(columns=["DUT 1 - dMax Temp","DUT 1 - dAvg Temp","DUT 2 - dMax Temp","DUT 2 - dAvg Temp"])
    newRow.loc[0]=[D1MaxAverage,D1AvgAverage,D2MaxAverage,D2AvgAverage]
    newRow.loc[1]=[D1MaxSTD,D1AvgSTD,D2MaxSTD,D2AvgSTD]
    newRow=newRow.rename(index={0:"Average",1:"STD"})

    #Add new rows
    finalFrame=finalFrame.append(newRow)
    
    #Display Table
    pd.set_option("display.max_rows", None, "display.max_columns", None,'display.expand_frame_repr', False)
    print(finalFrame)
    

    #Display Graph
    ax.grid()
    ax.legend()
    ax.set_xlabel("Data Point Number (Index)")
    ax.set_ylabel("Temperature (deg C)")
    plt.show()


main()