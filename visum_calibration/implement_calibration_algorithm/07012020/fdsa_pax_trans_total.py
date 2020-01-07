'''
Created on 7 Jan 2020

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
verFile = "2_Network_Final.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

#save results 
result_df_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\test_1422.csv"

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

stopPointListDf_Observed = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\network\\stop_point_total_pax_transfer_observed.csv")

#todo rename the columns e.g. "variableName_Obs"









max_iterations = 300

alpha = 1.0
gamma = 0.166666667
c = 1.4
a = 0.9
A = 30.0

#initial_guess = [float(0.001), float(0.001), float(0.001), float(0.001)] #poor estimates
#initial_guess = [float(1.8), float(2.8), float(3.8), float(5.8)] #better estimates
initial_guess = [0.3472315, 0.001, 0.175536, 1.0454] #results from run 1 plugged in as initial estimates and run the simulation again
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
