'''
Created on 17 Mar 2020

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

run_1_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_1\\run_1_rmsn_hp_set_13_spsa_29022020.csv")
run_2_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_2\\run_2_rmsn_hp_set_13_spsa_07032020.csv")
run_3_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_3\\run_3_rmsn_hp_set_13_spsa_11032020.csv")

# get first 80 records

run_1_df = run_1_df[1:80]
run_2_df = run_2_df[1:80]
run_3_df = run_3_df[1:80]

iteration_list = run_1_df.Iteration.tolist()

#plt.style.use("seaborn-colorblind")
plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
fig, ax = plt.subplots()

ax.plot(iteration_list, run_2_df.RMSN, label = 'In-vehicle = 1', color = 'r', alpha=0.8)
ax.plot(iteration_list, run_1_df.RMSN, label = 'Transfer penalty = 5min', color = 'lightgrey', alpha=0.7, linestyle='-.')
ax.plot(iteration_list, run_3_df.RMSN, label = 'All parameters', color = 'lightgrey', alpha=0.7, linestyle='-.')
ax.set_xlabel("Iteration")
ax.set_ylabel("RMSN")
ax.set_yticks(np.arange(3,8,0.5))
plt.legend()
plt.savefig("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\4_Report\\plots\\singapore_initial_calibration\\calibration_invehicle_1_highlighted.svg")
#plt.show()