import numpy as np
import pandas as pd
from tkinter import filedialog as fd
import time as t

#Load function integrated into main for ease of use
def main():
    #Load Multiple files
    fileNames=fd.askopenfilenames()

    #for loop load the data
    dataList=[]
    loadTime=0
    for name in fileNames:
        
        print("Loading new file: "+name)
        #Load a file, create dataframe
        t0=t.time()
        data=pd.read_csv(name,index_col=False)

        #Check columns
        print("Checking...")
        cols=data.columns
        toDel=[]
        for col in cols:
            if(np.count_nonzero(data[col])==0):
                toDel.append(col)
                
        #Trim dataframe
        print("Trimming...")
        data = data.drop(columns=toDel)
        
        #Load trimmed dataframe to csv
        #print("Compressing...")
        trimmedName=name.split("/")
        #compression_opts = dict(method='zip',archive_name=trimmedName[len(trimmedName)-1]) 
        #data.to_csv(name+'.zip', index=False,compression=compression_opts)

        data.to_csv(trimmedName[len(trimmedName)-1]+" - Output.csv")
        print("File Done!")

        t1=t.time()
        deltaT=t1-t0
        loadTime=loadTime+deltaT
        print("It took "+str(round(deltaT,3))+" seconds to process this file.")

    print("Finished loading and trimming files, total time: "+str(round(loadTime,3))+" seconds.")
    


main()
