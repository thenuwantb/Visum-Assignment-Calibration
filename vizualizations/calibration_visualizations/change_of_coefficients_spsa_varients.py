'''
Created on 28 Jan 2020

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('default')
import itertools

#This is to compare FDSA and SPSA with far estimates and close estimates - altogether 4 line plots in one plot
#load csvs as dataframes
 
spsa_vanila = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\1_net_2_hp_13_ob_1\\cleaned_data\\spsa_vanila_close_28012020_cleaned.csv")
spsa_adaptiveStep = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\2_mumford_1_hp_13_ob_2\\far_cleaned\\spsa_adaptive_step_far_29012020_cleaned.csv")
spsa_weight = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\2_mumford_1_hp_13_ob_2\\far_cleaned\\spsa_weight_far_29012020_cleaned.csv")
spsa_aStepWeight = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\2_mumford_1_hp_13_ob_2\\far_cleaned\\spsa_aStep_weight_far_29012020_cleaned.csv")

iteration_list = spsa_adaptiveStep.Iteration.tolist()
 
#spsa results to seperate lists

sv_inVehicleTime_est = spsa_vanila.invehicleTime_est.tolist()
sv_accessTime_est = spsa_vanila.accessTime_est.tolist()
sv_egressTime_est = spsa_vanila.egressTime_est.tolist()
sv_transferWalkingTime_est = spsa_vanila.walkingTime_est.tolist()
sv_originWaitTime_est = spsa_vanila.originWaitTime_est.tolist()
sv_transferWaitTime_est = spsa_vanila.transferWaitTime_est.tolist()


sw_inVehicleTime_est = spsa_weight.invehicleTime_est.tolist()
sw_accessTime_est = spsa_weight.accessTime_est.tolist()
sw_egressTime_est = spsa_weight.egressTime_est.tolist()
sw_transferWalkingTime_est = spsa_weight.walkingTime_est.tolist()
sw_originWaitTime_est = spsa_weight.originWaitTime_est.tolist()
sw_transferWaitTime_est = spsa_weight.transferWaitTime_est.tolist()
 

sa_inVehicleTime_est = spsa_adaptiveStep.invehicleTime_est.tolist()
sa_accessTime_est = spsa_adaptiveStep.accessTime_est.tolist()
sa_egressTime_est = spsa_adaptiveStep.egressTime_est.tolist()
sa_transferWalkingTime_est = spsa_adaptiveStep.walkingTime_est.tolist()
sa_originWaitTime_est = spsa_adaptiveStep.originWaitTime_est.tolist()
sa_transferWaitTime_est = spsa_adaptiveStep.transferWaitTime_est.tolist()

saw_inVehicleTime_est = spsa_aStepWeight.invehicleTime_est.tolist()
saw_accessTime_est = spsa_aStepWeight.accessTime_est.tolist()
saw_egressTime_est = spsa_aStepWeight.egressTime_est.tolist()
saw_transferWalkingTime_est = spsa_aStepWeight.walkingTime_est.tolist()
saw_originWaitTime_est = spsa_aStepWeight.originWaitTime_est.tolist()
saw_transferWaitTime_est = spsa_aStepWeight.transferWaitTime_est.tolist()
 
 
 
#multi line plot to see the change of in vehicle time estimate over the iterations
_prior = list(itertools.repeat(2.0,301))
    

_ = plt.plot(iteration_list, sv_originWaitTime_est, color = 'dimgrey',  linewidth = 1.0 , label = 'Vanila SPSA') #color = 'red'
_ = plt.plot(iteration_list, sw_originWaitTime_est, color = 'orangered', linewidth = 1.2 , label = 'Weight') #color = 'darkorange'
_ = plt.plot(iteration_list, sa_originWaitTime_est, color = 'dodgerblue', linewidth = 1.2, label = 'Adaptive Step') #color = 'royalblue'
#_ = plt.plot(iteration_list, saw_originWaitTime_est, color = 'mediumseagreen', linewidth = 1.2 , label = 'Adaptive Step & Weight') #color = 'seagreen'

_ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Observed Value')
 
 
_ = plt.xlabel("Iteration")
_ = plt.ylabel('Estimated value the coefficient')
_ = plt.suptitle("Change of Origin Wait Time Coefficient")
_ = plt.title("alpha = 0.602, gamma = 0.101, c = 1.419, a = 4.833, A = 30.0", fontsize = 10)
 
_ = plt.legend()
     
plt.show()
#savepath = 'C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\28012020_evaluate_spsa_varients\\results\\1_net_2_hp_13_ob_1\\cleaned_data\\inVehicle.svg'
#plt.draw()
#plt.savefig(savepath, bbox_inches = 'tight')   
