'''
Created on 19 Jan 2020

@author: thenuwan.jayasinghe
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
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network"
verFile = "Network_2_20200107_TJ_Final.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# save results 
result_df_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\10_hyper_parameter_set_17\\hp_set17_SPSA_far_15012020.csv"

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observedStopPointDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\stop_point_total_pax_transfer_observed_10012020.csv")

changeColNamesStopPointDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs", "PassTransDir(AP)" : "PassTransDir(AP)_Obs", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Obs",
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Obs", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Obs"}

observedStopPointDf = observedStopPointDf.rename(columns=changeColNamesStopPointDic)

observedTransferWalkTimeDf = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\Transfers_and_Walk_Times_Within_Stop_13012019.csv")
changeColNamesTransferWalkTime = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Obs"}
observedTransferWalkTimeDf = observedTransferWalkTimeDf.rename(columns=changeColNamesTransferWalkTime)

max_iterations = 300

alpha = 0.602
gamma = 0.101
c = 0.6
a = 3.7
A = 30.0
C = 0   # added as an experiment - to control the behaviour of ck - (0 = no impact)

# Order : In-vehicle time, Access time, Egress time, Walk time, Origin wait time, Transfer wait time
initial_guess = [2.0, 2.8, 3.0, 1.0, 1.5, 2.0]  # [2.0, 2.8, 3.0, 1.0, 1.5, 2.0] # far [5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
initial_cost = sg.runAssignmentCalculateErrorRMSN(Visum, initial_guess, observedStopPointDf, observedTransferWalkTimeDf)

initial_cost = sg.runAssignmentCalculateErrorRMSN(Visum, initial_guess, observedStopPointDf, observedTransferWalkTimeDf)

print initial_guess, initial_cost
plot_dict = OrderedDict()
plot_dict = {0:[initial_cost, initial_guess]}

u = np.copy(initial_guess)

np.random.seed(55)
# np.random.seed(100)
# np.random.seed(159)
# np.random.seed(486)
# np.random.seed(999)

# measure time - start
t_start = timeit.default_timer()

for k in range(max_iterations):
    
    ak = a / (A + k + 1) ** alpha
    ck = c / (C + k + 1) ** gamma
    
    # Step 2 - Generation of simultaneous perturbation vector

    deltaK = np.random.choice([-1, 1], size=len(u), p=[0.5, 0.5])  # delta_k = np.array([1,-1])
    
    # looping over each element and check whether it is in range (0,9) after the change
    increase_u = np.copy(u)
    decrease_u = np.copy(u)
    
    for i in range(len(increase_u)):
        if u[i] + ck * deltaK[i] > 0 and u[i] + ck * deltaK[i] <= 9.9:
            increase_u[i] = u[i] + ck * deltaK[i]
        else:
            increase_u[i] = u[i]
    
    for j in range(len(decrease_u)):
        if u[j] - ck * deltaK[j] > 0 and u[j] - ck * deltaK[j] <= 9.9:
            decrease_u[j] = u[j] - ck * deltaK[j]
        else:
            decrease_u[j] = u[j]
    
    # Step 3 - Function evaluation
    cost_increase = sg.runAssignmentCalculateErrorRMSN(Visum, increase_u, observedStopPointDf, observedTransferWalkTimeDf)
    cost_decrease = sg.runAssignmentCalculateErrorRMSN(Visum, decrease_u, observedStopPointDf, observedTransferWalkTimeDf)
    
    # Step 4 - Gradient approximation
    gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
    
    # Step 5 - Update u estimate
    old_u = np.copy(u)
    
    #--------------fix 05122019---------------------------------
    gk_step_size = ak * gk
    
    for m in range(len(old_u)):
        if old_u[m] - gk_step_size[m] >= 0 and old_u[m] - gk_step_size[m] <= 9.9:
            u[m] = old_u[m] - gk_step_size[m]
            
        else:
            u[m] = old_u[m]
    
    cost_new = vlc.calcErrorWithSimulatedValues_StopPoints(Visum, observedStopPointDf, u)
    #--------------fix 05122019---------------------------------
     
    print k 
    print cost_new
    print u
    estimate_to_dict = np.copy(u)
    
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
