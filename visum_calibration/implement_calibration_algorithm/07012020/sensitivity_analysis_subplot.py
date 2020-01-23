'''
Created on 19 Jan 2020

@author: thenuwan.jayasinghe
'''
from collections import OrderedDict
from custom_visum_functions.open_close_visum import open_close as ocv
from custom_visum_functions.visum_list_calculations import list_calculations as vlc
from custom_visum_functions.visum_list_calculations import simulated_values_generator as sg
from numpy import shape
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import win32com.client as com
import timeit
import copy

# Load Visum Version and create a Network Object
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\network\\network2"
verFile = "Network_2.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\network\\network2\\stop_point_obs.csv")

changeColNamesStopPointDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs", "PassTransDir(AP)" : "PassTransDir(AP)_Obs", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Obs",
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Obs", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Obs"}

observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesStopPointDic)

observedRouteListDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\network\\network2\\line_route_obs.csv")
changeColNamedDic_RouteList = {"PTripsUnlinked0(AP)":"PTripsUnlinked0(AP)_Obs", "PTripsUnlinked1(AP)" : "PTripsUnlinked1(AP)_Obs"}
observedRouteListDf = observedRouteListDf.rename(columns=changeColNamedDic_RouteList)
observedRouteListDf["LineName"] = observedRouteListDf["LineName"].astype(str)
observedRouteListDf["Name"] = observedRouteListDf["Name"].astype(str)

#Create dataframe and assign values
df_rmsn_columns = ['coefficient', 'inVeh','access', 'egress', 'traWalk', 'oriWait', 'traWait']
df_rmsn = pd.DataFrame(columns = df_rmsn_columns)
parameterValueList = (np.arange(0.0 , 9.9, 0.1)).tolist()

parameterValueSeries = pd.Series(parameterValueList)

df_rmsn['coefficient'] = parameterValueSeries.values

#print df_rmsn.head(10) - values are assigned correctly


#Save simulated rmsn values to the dataframe
estimateList = [1.0, 2.0, 2.0, 1.5, 2.0, 3.0]

for estimate in range(len(estimateList)):
    estimates = copy.copy(estimateList)
    #print estimates
    
    for i in range(len(parameterValueList)):
        #print i
        
        estimates[estimate] = parameterValueList[i]
        print estimates
        rmsnValue = sg.runAssignmentCalculateErrorRMSN(Visum, estimates, obsStopPoints = observedStopPointDf, obsLineRoutes = observedRouteListDf)
        df_rmsn.at[i, df_rmsn_columns[estimate+1]] = rmsnValue
        
#===============================================================================
# plt.plot(df_rmsn['coefficient'], df_rmsn['inVeh'])
# plt.show()
#===============================================================================

df_rmsn.to_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\results\\1_hp_set_13\\sensitivity_results.csv")

#creating subplot
titleList = ["In-Vehicle Time", "Access Time", "Egress Time", "Transfer Walk Time", "Origin Wait Time", "Transfer Wait Time"]
df_rmsn_para = df_rmsn[['inVeh','access', 'egress', 'traWalk', 'oriWait', 'traWait']]
fig, axes = plt.subplots(nrows = 2, ncols = 3)



xlim = (0, 10)
ylim = (0, 15)



fig.suptitle('Sensitivity Analysis')

for col, ax in zip(df_rmsn_para.columns, axes.flatten()):
    ax.plot(df_rmsn['coefficient'], df_rmsn_para[col])

plt.setp(axes, xlim = xlim, ylim = ylim)   
plt.show()

