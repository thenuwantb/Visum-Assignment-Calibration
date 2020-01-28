'''
Created on 23 Jan 2020

@author: thenuwan.jayasinghe
@note: Implementing adaptive step size with FDSA algorithm - Ito, Keiichi; Dhaene, Tom (2016)
'''
from collections import OrderedDict
from custom_visum_functions.open_close_visum import open_close as ocv
from custom_visum_functions.visum_list_calculations import list_calculations as vlc
from custom_visum_functions.visum_list_calculations import simulated_values_generator as sg
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import win32com.client as com
import timeit

# Load Visum Version and create a Network Object
path = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients"
verFile = "network\\network2\\Network_2.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# save results 
results_save = "results\\1_net_2_hp_13_ob_1\\spsa_aStep_weight_close_28012020.csv"
result_df_save_as = os.path.join(path, results_save)

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv(os.path.join(path, "network\\network2\\stop_point_obs.csv"))

changeColNamesStopPointDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs", "PassTransDir(AP)" : "PassTransDir(AP)_Obs", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Obs",
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Obs", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Obs"}

observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesStopPointDic)

observedRouteListDf = pd.read_csv(os.path.join(path, "network\\network2\\line_route_obs.csv"))
changeColNamedDic_RouteList = {"PTripsUnlinked0(AP)":"PTripsUnlinked0(AP)_Obs", "PTripsUnlinked1(AP)" : "PTripsUnlinked1(AP)_Obs"}
observedRouteListDf = observedRouteListDf.rename(columns=changeColNamedDic_RouteList)
observedRouteListDf["LineName"] = observedRouteListDf["LineName"].astype(str)
observedRouteListDf["Name"] = observedRouteListDf["Name"].astype(str)

max_iterations = 300

alpha = 0.602
gamma = 0.101
c = 1.419123356
a = 4.83338664027225
A = 30.0
C = 0   # added as an experiment - to control the behaviour of ck - (0 = no impact)

# Order : In-vehicle time, Access time, Egress time, Walk time, Origin wait time, Transfer wait time
initial_guess = [2.0, 2.8, 3.0, 1.0, 1.5, 2.0]  # [2.0, 2.8, 3.0, 1.0, 1.5, 2.0] # far [5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
parameter_weights = [0.263847468, 1.0, 0.527366201, 0.929654002, 0.521260619, 0.510245914]  #calculated based on standard deviation of each parameter from the sensitivity analysis
initial_cost = sg.runAssignmentCalculateErrorRMSN(Visum, initial_guess, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
print initial_guess, initial_cost

plot_dict = OrderedDict()
plot_dict = {0:[initial_cost, initial_guess]}

current_estimate = np.copy(initial_guess)
best_estimate = np.copy(initial_guess)
best_rmsn = np.copy(initial_cost)

np.random.seed(55)

# measure time - start
t_start = timeit.default_timer()

for k in range(max_iterations):
    
    ak = a / (A + k + 1) ** alpha
    ck = c / (C + k + 1) ** gamma
    
    # Step 2 - Generation of simultaneous perturbation vector

    deltaK = np.random.choice([-1, 1], size=len(current_estimate), p=[0.5, 0.5])  # delta_k = np.array([1,-1])
    
    # looping over each element and check whether it is in range (0,9) after the change
    increase_u = np.copy(current_estimate)
    decrease_u = np.copy(current_estimate)
    
    for i in range(len(increase_u)):
        if current_estimate[i] + ck * deltaK[i] > 0 and current_estimate[i] + ck * deltaK[i] <= 9.9:
            increase_u[i] = current_estimate[i] + ck * deltaK[i] * parameter_weights[i]
        else:
            increase_u[i] = current_estimate[i]
    
    for j in range(len(decrease_u)):
        if current_estimate[j] - ck * deltaK[j] > 0 and current_estimate[j] - ck * deltaK[j] <= 9.9:
            decrease_u[j] = current_estimate[j] - ck * deltaK[j] * parameter_weights[i]
        else:
            decrease_u[j] = current_estimate[j]
    
    # Step 3 - Function evaluation
    cost_increase = sg.runAssignmentCalculateErrorRMSN(Visum, increase_u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    cost_decrease = sg.runAssignmentCalculateErrorRMSN(Visum, decrease_u, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    
    # Step 4 - Gradient approximation
    gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
    
    # Step 5 - Update current_estimate estimate
    previous_estimate = np.copy(current_estimate)
    
    
    gk_step_size = ak * gk
    gk_step_size_weights = [gk * weight for gk, weight in zip(gk_step_size, parameter_weights)]
    
    
    #===========================================================================
    # for m in range(len(previous_estimate)):
    #         if previous_estimate[m] - gk_step_size_weights[m] >= 0 and previous_estimate[m] - gk_step_size_weights[m] <= 9.9:
    #             current_estimate[m] = previous_estimate[m] - gk_step_size_weights[m]
    #  
    #         else:
    #             current_estimate[m] = best_estimate[m] #earlier : current_estimate[m] = previous_estimate[m]
    #===========================================================================
                
    if (min(cost_increase, cost_decrease) - initial_cost) >= 0:
        current_estimate = np.copy(best_estimate)
        a = a*0.5
        print "xxx"
    else:
          
        for m in range(len(previous_estimate)):
            if previous_estimate[m] - gk_step_size_weights[m] >= 0 and previous_estimate[m] - gk_step_size_weights[m] <= 9.9:
                current_estimate[m] = previous_estimate[m] - gk_step_size_weights[m]
      
            else:
                current_estimate[m] = best_estimate[m] #earlier : current_estimate[m] = previous_estimate[m]
            
            
    cost_new = sg.runAssignmentCalculateErrorRMSN(Visum, current_estimate, obsStopPoints=observedStopPointDf, obsLineRoutes = observedRouteListDf)
    
    
    if cost_new < best_rmsn:
        best_rmsn = cost_new
        best_estimate = np.copy(current_estimate) 
    
    print k
    print cost_new
    print current_estimate
    print best_estimate
    
    estimate_to_dict = np.copy(current_estimate)
    
    plot_dict[k + 1] = [cost_new, estimate_to_dict]

t_duration = timeit.default_timer() - t_start
print "Duration = " + str(t_duration)

# saving values to a Data Frame
results_df = pd.DataFrame()

# Creation of the plot - and then save the values to a Data Frame  - change made on 10122019
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

# Plot
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()
