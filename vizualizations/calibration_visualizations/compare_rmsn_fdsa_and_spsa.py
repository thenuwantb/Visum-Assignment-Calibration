'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fdsa_hp_set_12 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\19012020\\results\\2_hp_set_18\\hp_set18_FDSA_close_20012020_cleaned.csv")
spsa_hp_set_12 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\19012020\\results\\2_hp_set_18\\hp_set18_SPSA_close_20012020_cleaned.csv")

# ===============================================================================
# fdsa_hp_set_4 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\hyper_parameter_set_4\\fdsa_far_hp_set_4_run_1.csv")
# spsa_hp_set_4 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\hyper_parameter_set_4\\spsa_far_hp_set_4_run_1.csv")
# ===============================================================================

fdsa_hp_set_12_rmsn = fdsa_hp_set_12.RMSN.tolist()
spsa_hp_set_12_rmsn = spsa_hp_set_12.RMSN.tolist()

# ===============================================================================
# fdsa_hp_set_4_rmsn = fdsa_hp_set_4.RMSN.tolist()
# spsa_hp_set_4_rmsn = spsa_hp_set_4.RMSN.tolist()
# ===============================================================================


fig, ax = plt.subplots()
iterations_list = fdsa_hp_set_12.Iteration.tolist()

_ = plt.plot(iterations_list, fdsa_hp_set_12_rmsn, linestyle='-', color='royalblue',
             label="Hyper parameter set 18 (FDSA)")
_ = plt.plot(iterations_list, spsa_hp_set_12_rmsn, linestyle='--', color='red', label="Hyper parameter set 18 (SPSA)")
# ===============================================================================
# _ = plt.plot(iterations_list, fdsa_hp_set_4_rmsn, color = 'royalblue', label = "Hyper parameter set 4 (FDSA)")
# _ = plt.plot(iterations_list, spsa_hp_set_4_rmsn, color = 'red', label = "Hyper parameter set 4 (SPSA)")
# ===============================================================================
# ax.set_xticks(np.arange(0, 4, 0.5))
ax.set_yticks(np.arange(0, 4.5, 0.5))
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.title("Close Estimates", fontsize=10)
plt.suptitle("RMSN : PassTransAlightWalk + PassTransWalkBoard + PTripsUnlinked")

plt.legend()

savepath = 'C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\19012020\\results\\2_hp_set_18\\change_of_rmsn_hp_18_close.svg'
plt.draw()
# plt.show()
plt.savefig(savepath, bbox_inches='tight')
