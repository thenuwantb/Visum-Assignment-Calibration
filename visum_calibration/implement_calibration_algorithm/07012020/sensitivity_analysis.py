'''
Created on 9 Jan 2020

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

# Load Visum Version and create a Network Object
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network"
verFile = "Network_2_20200107_TJ_Final.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\stop_point_total_pax_transfer_observed_10012020.csv")
changeColNamesDic = {"PassTransTotal(AP)": "PassTransTotal(AP)_Obs", "PassTransDir(AP)": "PassTransDir(AP)_Obs",
                     "PassTransWalkBoard(AP)": "PassTransWalkBoard(AP)_Obs",
                     "PassTransAlightWalk(AP)": "PassTransAlightWalk(AP)_Obs",
                     "TransferWaitTime(AP)": "TransferWaitTime(AP)_Obs"}
observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesDic)

observedTransferWalkTimeDf = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\Transfers_and_Walk_Times_Within_Stop_13012019.csv")
changeColNamesTransferWalkTime = {"PassTransTotal(AP)": "PassTransTotal(AP)_Obs"}
observedTransferWalkTimeDf = observedTransferWalkTimeDf.rename(columns=changeColNamesTransferWalkTime)

observedConnectorVolumesDf = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\connectors_observed_14012019.csv")
changeColNamesConnectors = {"VolPersPuT(AP)": "VolPersPuT(AP)_Obs"}
observedConnectorVolumesDf = observedConnectorVolumesDf.rename(columns=changeColNamesConnectors)

plot_dict = OrderedDict()
parameterValueList = np.arange(0.0, 9.9, 0.1)
print type(parameterValueList)

# Order : In-vehicle time, Access time, Egress time, Walk time, Origin wait time, Transfer wait time
estimateList = [1.0, 2.0, 2.0, 1.5, 2.0, 3.0]
titleList = ["In-Vehicle Time", "Access Time", "Egress Time", "Transfer Walk Time", "Origin Wait Time",
             "Transfer Wait Time"]

for i in range(len(parameterValueList)):
    # print i
    estimateList[5] = parameterValueList[i]

    print estimateList

    rmsnValue = sg.runAssignmentCalculateErrorRMSN(Visum, estimateList, observedStopPointDf, observedTransferWalkTimeDf)

    plot_dict[i] = rmsnValue

# creation of the plot
coefficient_values = parameterValueList.tolist()
rmsn_values = []

for key, value in plot_dict.items():
    rmsn_values.append(value)

# customize the grid

fig, ax = plt.subplots()

plt.plot(coefficient_values, rmsn_values)
ax.set_xticks(np.arange(0, 10.0, 1))
ax.set_yticks(np.arange(0, 5.5, 0.5))
ax.grid(which='major', linestyle='-', linewidth='0.5')
ax.grid(which='minor', linestyle='-', linewidth='0.2')

plt.xlabel("Coefficient value of the parameter", fontsize=10)
plt.ylabel("RMSN", fontsize=10)
plt.title("Transfer Wait Time", fontsize=12)

savepath = 'C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\sensitivity_analysis\\17012020 - report to Moeid\\transfer_wait.svg'
plt.draw()
# plt.show()
plt.savefig(savepath, bbox_inches='tight')
