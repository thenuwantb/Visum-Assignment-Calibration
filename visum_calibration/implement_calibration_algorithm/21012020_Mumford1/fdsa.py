'''
Created on 21 Jan 2020

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
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\21012020_Mumford1\\network"
verFile = "Mumford1_100_100_0.9_0.005_50_itr6_itrcap6_Solution_3.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# save results 
result_df_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\21012020_Mumford1\\results\\2_hp_set_20\\hp_20_fdsa_close.csv"

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\21012020_Mumford1\\network\\stopPoint_observed.csv")

changeColNamesStopPointDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs", "PassTransDir(AP)" : "PassTransDir(AP)_Obs", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Obs",
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Obs", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Obs"}

observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesStopPointDic)

observedRouteListDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\21012020_Mumford1\\network\\lineRoute_observed.csv")
changeColNamedDic_RouteList = {"PTripsUnlinked0(AP)":"PTripsUnlinked0(AP)_Obs", "PTripsUnlinked1(AP)" : "PTripsUnlinked1(AP)_Obs"}
observedRouteListDf = observedRouteListDf.rename(columns=changeColNamedDic_RouteList)
observedRouteListDf["LineName"] = observedRouteListDf["LineName"].astype(str)
observedRouteListDf["Name"] = observedRouteListDf["Name"].astype(str)

max_iterations = 300

alpha = 0.602
gamma = 0.101
c = 0.160877492522691
a = 1.61112888009075
A = 30.0
C = 0  # added as an experiment - to control the behaviour of ck - (0 = no impact)


# Order : In-vehicle time, Access time, Egress time, Walk time, Origin wait time, Transfer wait time
initial_guess = [2.0, 1.5, 2.0]   # close [2.0, 2.8, 3.0, 1.0, 1.5, 2.0] # far [5.0, 5.0, 5.0, 5.0, 5.0, 5.0] #exact [1.0, 2.0, 2.0, 1.5, 2.0, 3.0] #farmost [9.0,9.0,9.0,9.0,9.0.9.0]
initial_cost = sg.runAssignmentCalculateErrorRMSN(Visum, initial_guess, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)

print initial_guess, initial_cost
plot_dict = OrderedDict()
plot_dict = {0:[initial_cost, initial_guess]}

u = np.copy(initial_guess)

# measure time - start
t_start = timeit.default_timer()

for k in range(max_iterations):
    
    ak = a / ((A + k + 1) ** alpha)
    ck = c / ((C + k + 1) ** gamma)
    
    gk = np.zeros(shape(u)[0])
    
    for i in range(shape(gk)[0]):
        
        # Step 2: Generate perturbations one parameter at a time. 
        
        increase_u = np.copy(u)
        
        if increase_u[i] + ck >= 0 and increase_u[i] + ck <= 9.9 :
            increase_u[i] += ck
        
        decrease_u = np.copy(u)
        if decrease_u[i] - ck >= 0 and decrease_u[i] - ck <= 9.9 :
            decrease_u[i] -= ck
        
        # Step 3: Function evaluation

        cost_increase = sg.runAssignmentCalculateErrorRMSN(Visum, increase_u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    
        cost_decrease = sg.runAssignmentCalculateErrorRMSN(Visum, decrease_u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
        
        # Step 4: Gradient Approximation
        gk[i] = (cost_increase - cost_decrease) / (2.0 * ck)
        
    old_u = np.copy(u)
    gk_step_size = ak * gk
    
    # Step 5 : Update u estimate
    
    for m in range(len(old_u)):
        if old_u[m] - gk_step_size[m] >= 0 and old_u[m] - gk_step_size[m] <= 9.9:
            u[m] = old_u[m] - gk_step_size[m]
            
        else:
            u[m] = old_u[m]
            print m
            print "xx"
    
    #cost_new = vlc.calcErrorWithSimulatedValues_StopPoints(Visum, observedStopPointDf, u)
    cost_new = sg.runAssignmentCalculateErrorRMSN(Visum, u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    
    print k
    print cost_new
    print u
    estimate_to_dict = np.copy(u)
    plot_dict[k + 1] = [cost_new, estimate_to_dict]
    
t_duration = timeit.default_timer() - t_start
print "Duration = " + str(t_duration)

# saving values to a Data Frame
results_df = pd.DataFrame()

# Creation of the plot
iteration_id = []
cost_value = []
estimate_list = []

for key, value in plot_dict.items():
    iteration_id.append(key)
    cost_value.append(value[0])
    estimate_list.append(value[1])

results_df['Iteration'] = iteration_id
results_df['RMSN'] = cost_value
results_df['estimate'] = estimate_list

results_df.to_csv(result_df_save_as)
    
# print y_val
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()
