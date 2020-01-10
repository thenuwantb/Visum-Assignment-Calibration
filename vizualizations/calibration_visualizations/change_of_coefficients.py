'''
Created on 10 Jan 2020

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt
import itertools

#load csvs as dataframes


spsa_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_14\\hp_set14_SPSA_10012020_cleaned.csv")
fdsa_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_14\\hp_set14_FDSA_10012020_cleaned.csv")

iteration_list = fdsa_df.Iteration.tolist()

#spsa results to seperate lists

s_inVehicleTime_est = spsa_df.invehicleTime_est.tolist()
s_accessTime_est = spsa_df.accessTime_est.tolist()
s_egressTime_est = spsa_df.egressTime_est.tolist()
s_transferWalkingTime_est = spsa_df.walkingTime_est.tolist()
s_originWaitTime_est = spsa_df.originWaitTime_est.tolist()
s_transferWaitTime_est = spsa_df.transferWaitTime_est.tolist()

#fdsa results to seperate lists
f_inVehicleTime_est = fdsa_df.invehicleTime_est.tolist()
f_accessTime_est = fdsa_df.accessTime_est.tolist()
f_egressTime_est = fdsa_df.egressTime_est.tolist()
t_transferWalkingTime_est = fdsa_df.walkingTime_est.tolist()
f_originWaitTime_est = fdsa_df.originWaitTime_est.tolist()
f_transferWaitTime_est = fdsa_df.transferWaitTime_est.tolist()



#multi line plot to see the change of in vehicle time estimate over the iterations
_prior = list(itertools.repeat(3.0,301))
   
_ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Target')
_ = plt.plot(iteration_list, f_transferWaitTime_est, linewidth = 1, color = 'royalblue', label = 'FDSA')
_ = plt.plot(iteration_list, s_transferWaitTime_est, linestyle = '--',linewidth = 1, color = 'red', label = 'SPSA')


_ = plt.xlabel("Iteration")
_ = plt.ylabel('Estimated value the coefficient')
_ = plt.title("Change of Transfer Wait Time Coefficient")
_ = plt.legend()
 
#plt.savefig('Inveh_Time_change_600dpi', dpi = 600)
    
plt.show()

#===============================================================================
# #multi line plot to see the change of walking time estimate over the iterations
# _prior = list(itertools.repeat(2.0,301))
#   
# _ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Target')
# _ = plt.plot(iteration_list, ff_walkingTime_est,  linewidth = 1, color = 'royalblue', label = 'FDSA')
# _ = plt.plot(iteration_list, fc_walkingTime_est,  linewidth = 1, color = 'royalblue')
# _ = plt.plot(iteration_list, sf_walkingTime_est, linestyle = '--',linewidth = 1, color = 'red', label = 'SPSA')
# _ = plt.plot(iteration_list, sc_walkingTime_est, linestyle = '--',linewidth = 1, color = 'red')
# _ = plt.xlabel("Iteration")
# _ = plt.ylabel('Estimated value of the coefficient')
# _ = plt.title("Walk Time")
# _ = plt.legend() 
# 
# plt.savefig('Walk_Time_change_600dpi', dpi = 600)
#    
# plt.show()
#===============================================================================

#===============================================================================
# #multi line plot to see the change of Origin wait time estimate over the iterations
# _prior = list(itertools.repeat(3.0,301))
#   
# _ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Target')
# _ = plt.plot(iteration_list, ff_originWaitTime_est,  linewidth = 1, color = 'royalblue', label = 'FDSA')
# _ = plt.plot(iteration_list, fc_originWaitTime_est, linewidth = 1, color = 'royalblue')
# _ = plt.plot(iteration_list, sf_originWaitTime_est, linestyle = '--', linewidth = 1, color = 'red', label = 'SPSA')
# _ = plt.plot(iteration_list, sc_originWaitTime_est, linestyle = '--', linewidth = 1, color = 'red')
# _ = plt.xlabel("Iteration")
# _ = plt.ylabel('Estimated value of the coefficient')
# _ = plt.title("Origin Wait Time")
# _ = plt.legend()
# 
# plt.savefig('Origin_Wait_Time_change_600dpi', dpi = 600)
#    
# plt.show()
#===============================================================================

#===============================================================================
# #multi line plot to see the change of transfer wait time estimate over the iterations
# _prior = list(itertools.repeat(5.0,301))
#   
# _ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Target')
# _ = plt.plot(iteration_list, ff_transferWaitTime_est, linewidth = 1, color = 'royalblue', label = 'FDSA')
# _ = plt.plot(iteration_list, fc_transferWaitTime_est, linewidth = 1, color = 'royalblue')
# _ = plt.plot(iteration_list, sf_transferWaitTime_est, linestyle = '--',linewidth = 1, color = 'red', label = 'SPSA')
# _ = plt.plot(iteration_list, sc_transferWaitTime_est, linestyle = '--',linewidth = 1, color = 'red')
# _ = plt.xlabel("Iteration")
# _ = plt.ylabel('Estimated value of the coefficient')
# _ = plt.title("Transfer Wait Time")
# _ = plt.legend()
# 
# plt.savefig('Trasfer_Wait_Time_change_600dpi', dpi = 600)
#    
# plt.show()
#===============================================================================