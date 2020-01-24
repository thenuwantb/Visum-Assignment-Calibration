'''
Created on 23 Jan 2020

@author: thenuwan.jayasinghe
@note: Implementing adaptive step size with FDSA algorithm - Ito, Keiichi; Dhaene, Tom (2016)
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
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\network\\Mumford1"
verFile = "Mumford1_100_100_0.9_0.005_50_itr6_itrcap6_Solution_3.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# save results 
result_df_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\results\\4_Mumford1\\1_hp_set_23\\hp_set_23_fdsa_as.csv"

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\network\\Mumford1\\stopPoint_observed.csv")

changeColNamesStopPointDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs", "PassTransDir(AP)" : "PassTransDir(AP)_Obs", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Obs",
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Obs", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Obs"}

observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesStopPointDic)

observedRouteListDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\23012020_adaptive_step\\network\\Mumford1\\lineRoute_observed.csv")
changeColNamedDic_RouteList = {"PTripsUnlinked0(AP)":"PTripsUnlinked0(AP)_Obs", "PTripsUnlinked1(AP)" : "PTripsUnlinked1(AP)_Obs"}
observedRouteListDf = observedRouteListDf.rename(columns=changeColNamedDic_RouteList)
observedRouteListDf["LineName"] = observedRouteListDf["LineName"].astype(str)
observedRouteListDf["Name"] = observedRouteListDf["Name"].astype(str)
max_iterations = 300

alpha = 0.602
gamma = 0.101
c = 0.268129154204486
a = 0.25
A = 5.0
C = 0  # added as an experiment - to control the behaviour of ck - (0 = no impact)


# Order : In-vehicle time, Access time, Egress time, Walk time, Origin wait time, Transfer wait time
initial_guess = [0.89246464, 2.82970775, 1.82521672]  # close [2.0, 2.8, 3.0, 1.0, 1.5, 2.0] # far [5.0, 5.0, 5.0, 5.0, 5.0, 5.0] #exact [1.0, 2.0, 2.0, 1.5, 2.0, 3.0] #farmost [9.0,9.0,9.0,9.0,9.0.9.0]
initial_cost = sg.runAssignmentCalculateErrorRMSN(Visum, initial_guess, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)

#Tracking the test value for the objective function

print initial_guess, initial_cost
plot_dict = OrderedDict()
plot_dict = {0:[initial_cost, initial_guess]}

current_estimate = np.copy(initial_guess)
best_estimate = np.copy(initial_guess)
best_rmsn = np.copy(initial_cost)

# measure time - start
t_start = timeit.default_timer()

for k in range(max_iterations):
    
    ak = a / ((A + k + 1) ** alpha)
    ck = c / ((C + k + 1) ** gamma)
    
    gk = np.zeros(shape(current_estimate)[0])
    
    for i in range(shape(gk)[0]):
        
        # Step 2: Generate perturbations one parameter at a time. 
        
        increase_u = np.copy(current_estimate)
        
        if increase_u[i] + ck >= 0 and increase_u[i] + ck <= 9.9 :
            increase_u[i] += ck
        
        decrease_u = np.copy(current_estimate)
        if decrease_u[i] - ck >= 0 and decrease_u[i] - ck <= 9.9 :
            decrease_u[i] -= ck
        
        # Step 3: Function evaluation

        cost_increase = sg.runAssignmentCalculateErrorRMSN(Visum, increase_u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    
        cost_decrease = sg.runAssignmentCalculateErrorRMSN(Visum, decrease_u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
        
        # Step 4: Gradient Approximation
        gk[i] = (cost_increase - cost_decrease) / (2.0 * ck)
        
    previous_estimate = np.copy(current_estimate)
    gk_step_size = ak * gk
    
    # Step 5 : Update current_estimate estimate
    
    
    for m in range(len(previous_estimate)):
        if previous_estimate[m] - gk_step_size[m] >= 0 and previous_estimate[m] - gk_step_size[m] <= 9.9:
            current_estimate[m] = previous_estimate[m] - gk_step_size[m] 
            
        else:
            current_estimate[m] = best_estimate[m] #earlier : current_estimate[m] = previous_estimate[m]
            #print m
    
    cost_new = sg.runAssignmentCalculateErrorRMSN(Visum, current_estimate, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    
    if cost_new < best_rmsn:
        best_rmsn = cost_new
        best_estimate = np.copy(current_estimate) 
    
    
    
    print k
    print cost_new
    print current_estimate
    print best_estimate
    #print best_rmsn
    
    estimate_to_dict = np.copy(current_estimate)
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
