'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt

fdsa_hp_set_12 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_12\\test_08012020_12_FDSA.csv")
spsa_hp_set_12 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_12\\test_08012020_12_SPSA.csv")

#===============================================================================
# fdsa_hp_set_4 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\hyper_parameter_set_4\\fdsa_far_hp_set_4_run_1.csv")
# spsa_hp_set_4 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\hyper_parameter_set_4\\spsa_far_hp_set_4_run_1.csv")
#===============================================================================

fdsa_hp_set_12_rmsn = fdsa_hp_set_12.RMSN.tolist()
spsa_hp_set_12_rmsn = spsa_hp_set_12.RMSN.tolist()

#===============================================================================
# fdsa_hp_set_4_rmsn = fdsa_hp_set_4.RMSN.tolist()
# spsa_hp_set_4_rmsn = spsa_hp_set_4.RMSN.tolist()
#===============================================================================

iterations_list = fdsa_hp_set_12.Iteration.tolist()

_ = plt.plot(iterations_list, fdsa_hp_set_12_rmsn, linestyle = '-', color = 'royalblue', label = "Hyper parameter set 12 (FDSA)")
_ = plt.plot(iterations_list, spsa_hp_set_12_rmsn, linestyle = '--', color = 'red', label = "Hyper parameter set 12 (SPSA)")
#===============================================================================
# _ = plt.plot(iterations_list, fdsa_hp_set_4_rmsn, color = 'royalblue', label = "Hyper parameter set 4 (FDSA)")
# _ = plt.plot(iterations_list, spsa_hp_set_4_rmsn, color = 'red', label = "Hyper parameter set 4 (SPSA)")
#===============================================================================

plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.title("New Network - RMSN for Total Passenger Transfers")

plt.legend()
plt.show()