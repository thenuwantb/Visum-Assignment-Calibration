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

#test

# Load Visum Version and create a Network Object
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\1_VISUM_Simple"
verFile = "2_Simple_Network.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

stopPointListDf_Observed = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\1_VISUM_Simple\\stopPoint_obs.csv")
stopPointListDf_Observed['Key'] = stopPointListDf_Observed['Key'].astype(str)
stopPointListDf_Observed['Observed_Values'] = stopPointListDf_Observed['Observed_Values'].astype(float)

max_iterations = 300

alpha = 0.602
gamma = 0.101
a = 0.101
A = 0.193
c = 0.0277

initial_guess = [float(1.8), float(2.8), float(3.8), float(5.8)]
initial_cost = vlc.calcErrorStopPointSimulatedAndObserved(Visum, stopPointListDf_Observed, initial_guess)

plot_dict = OrderedDict()
plot_dict = {0:[initial_cost, initial_guess]}

u = np.copy(initial_guess)

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

# saving values to a Data Frame
results_df = pd.DataFrame()
df_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\1_VISUM_Simple\\FDSA_close_11122019_1003.csv"

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

results_df.to_csv(df_save_as)
    
# print y_val
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()
