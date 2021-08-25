#Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
import time as t

#def plotting(stuff):
    
    

def main():
    
    fileNames=fd.askopenfilenames()
    loadT = 0
    startT = t.time()
    print("Loading Files")
    cols=["Time (s)",
          "ICM2 - Ud (V)",
          "ICM2 - Uq (V)",
          "TC0 - DUT1 SCI50",
          "TC1 - DUT1 SCI60",
          "TC2 - DUT1 SCO40",
          "TC3 - DUT1 SWI50",
          "TC4 - DUT1 SWI60",
          "TC5 - DUT1 SWI70",
          "TC6 - DUT1 SWO40",
          "TC7 - DUT2 SCI50",
          "TC8 - DUT2 SCI60",
          "TC9 - DUT2 SCO40",
          "TC10 - DUT2 SWI50",
          "TC11 - DUT2 SWI60",
          "TC12 - DUT2 SWI70",
          "TC13 - DUT2 SWO40"]


    for name in fileNames:

        data = pd.read_csv(name,usecols=cols,index_col=False)
        data = data[::20]
        data.to_csv(name + ' Resampled.csv', index = False)

    endT = t.time()
    deltaT = endT - startT

    print("Done! Load Time: " + str(round(deltaT, 3)) + " seconds")

    fig,ax=plt.subplots()
    time=data["Time (s)"]

    print("Plotting Data")
    i=3
    while i < len(cols):
        ax.plot(time, data[cols[i]],label=cols[i])
        i = i + 1
        

    ud="ICM2 - Ud (V)"
    uq="ICM2 - Uq (V)"
    
    fig2,ax2=plt.subplots()
    
    ax2.plot(time,data[ud],label=ud)
    ax2.plot(time,data[uq],label=uq)

    ax2.grid()
    ax2.legend()

    ax.grid()
    ax.legend()

    print("Showing Plots...")
    plt.show()

main()
