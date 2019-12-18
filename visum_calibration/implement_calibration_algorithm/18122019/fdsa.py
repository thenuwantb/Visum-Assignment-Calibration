'''
Created on 18 Dec 2019

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
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\network"
verFile = "simple_network_11_stops.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

#save results 
result_df_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\hyper_parameter_set_4\\fdsa_far_hp_set_4_run_1.csv"

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

stopPointListDf_Observed = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\network\\stopPoint_obs.csv")
stopPointListDf_Observed['Key'] = stopPointListDf_Observed['Key'].astype(str)
stopPointListDf_Observed['Observed_Values'] = stopPointListDf_Observed['Observed_Values'].astype(float)

max_iterations = 300

alpha = 1
gamma = 0.166666667
c = 1.122462
a = 3.2
A = 30


initial_guess = [float(0.001), float(0.001), float(0.001), float(0.001)]
initial_cost = vlc.calcErrorStopPointSimulatedAndObserved(Visum, stopPointListDf_Observed, initial_guess)

plot_dict = OrderedDict()
plot_dict = {0:[initial_cost, initial_guess]}

u = np.copy(initial_guess)

#measure time - start
t_start = timeit.default_timer()

for k in range(max_iterations):
    
    ak = a / (A + k + 1)**alpha
    ck = c / (k + 1)**gamma
    
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
        cost_increase = vlc.calcErrorStopPointSimulatedAndObserved(Visum, stopPointListDf_Observed, increase_u)
    
        cost_decrease = vlc.calcErrorStopPointSimulatedAndObserved(Visum, stopPointListDf_Observed, decrease_u)
        
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
    
    cost_new = vlc.calcErrorStopPointSimulatedAndObserved(Visum, stopPointListDf_Observed, u)
    
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
results_df['Estimate'] = estimate_list

results_df.to_csv(result_df_save_as)
    
# print y_val
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()
