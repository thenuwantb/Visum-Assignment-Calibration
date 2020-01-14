'''
Created on 9 Jan 2020

@author: thenuwan.jayasinghe
'''
from collections import OrderedDict
from custom_visum_functions.open_close_visum import open_close as ocv
from custom_visum_functions.visum_list_calculations import list_calculations as vlc
from numpy import shape
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import win32com.client as com
import timeit

# Load Visum Version and create a Network Object
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network"
verFile = "Network_2_20200107_TJ_Final.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\stop_point_total_pax_transfer_observed_10012020.csv")
changeColNamesDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs", "PassTransDir(AP)" : "PassTransDir(AP)_Obs", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Obs",
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Obs", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Obs"}

observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesDic)

plot_dict = OrderedDict()
parameterValueList = np.arange(0 , 9.9, 0.1)
print type(parameterValueList)

# Order : In-vehicle time, Access time, Egress time, Walk time, Origin wait time, Transfer wait time
estimateList = [1.0, 2.0, 2.0, 1.5, 2.0, 3.0]
 
for i in range(len(parameterValueList)):
    print i
    estimateList[5] = parameterValueList[i]
      
    rmsnValue = vlc.calcErrorWithSimulatedValues_StopPoints(Visum, observedStopPointDf, estimateList)
      
    plot_dict[i] = rmsnValue
      
# creation of the plot
coefficient_values = parameterValueList.tolist()
rmsn_values = []
  
for key, value in plot_dict.items():
    rmsn_values.append(value)
      
plt.plot(coefficient_values, rmsn_values)
plt.xlim(-1, 10)
plt.ylim(-1, 10)

plt.title("RMSN with change of Transfer Wait Time coefficient")

plt.show()
     
