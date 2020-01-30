'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

spsa_vanila = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\1_net_2_hp_13_ob_1\\cleaned_data\\spsa_vanila_close_28012020_cleaned.csv")
spsa_adaptiveStep = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\1_net_2_hp_13_ob_1\\cleaned_data\\spsa_adaptive_step_close_28012020_cleaned.csv")
spsa_weight = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\1_net_2_hp_13_ob_1\\cleaned_data\\spsa_weight_close_28012020_cleaned.csv")
spsa_aStepWeight = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\1_net_2_hp_13_ob_1\\cleaned_data\\spsa_aStep_weight_close_28012020_cleaned.csv")


spsa_vanila_loss = spsa_vanila.RMSN.tolist()
spsa_adaptiveStep_loss = spsa_adaptiveStep.RMSN.tolist()
spsa_weight_loss = spsa_weight.RMSN.tolist()
spsa_aStepWeight_loss = spsa_aStepWeight.RMSN.tolist()

fig, ax = plt.subplots()
iterations_list = spsa_vanila.Iteration.tolist()

_ = plt.plot(iterations_list, spsa_vanila_loss, linewidth = 1.0, color = 'dimgrey', label = "Vanila SPSA")
_ = plt.plot(iterations_list, spsa_adaptiveStep_loss, linewidth = 1.2, color = 'dodgerblue', label = "Adaptive Step")
_ = plt.plot(iterations_list, spsa_weight_loss, linewidth = 1.2, color = 'orangered', label = "Weight")
_ = plt.plot(iterations_list, spsa_aStepWeight_loss, linewidth = 1.2, color = 'mediumseagreen', label = "Adaptive Step & Weight")

ax.set_yticks(np.arange(0, 8.0, 0.5))
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.title("alpha = 0.602, gamma = 0.101, c = 1.419, a = 4.833, A = 30.0", fontsize = 10)
plt.suptitle("Change of RMSN with varients of SPSA (Mumford1) - close initial estimates ")

plt.legend()

#savepath = 'C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\19012020\\results\\2_hp_set_18\\change_of_rmsn_hp_18_close.svg'
#plt.draw()
plt.show()
#plt.savefig(savepath, bbox_inches = 'tight')   
