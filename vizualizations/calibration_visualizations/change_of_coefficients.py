'''
Created on 10 Jan 2020

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt
import itertools

#This is to compare FDSA and SPSA with far estimates and close estimates - altogether 4 line plots in one plot
#load csvs as dataframes
 
spsa_close_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\9_hyper_parameter_set_16\\cleaned_data\\hp_set16_SPSA_close_14012020_cleaned.csv")
fdsa_close_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\9_hyper_parameter_set_16\\cleaned_data\\hp_set16_FDSA_close_14012020_cleaned.csv")

spsa_far_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\9_hyper_parameter_set_16\\cleaned_data\\hp_set16_SPSA_far_14012020_cleaned.csv")
fdsa_far_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\9_hyper_parameter_set_16\\cleaned_data\\hp_set16_FDSA_far_14012020_cleaned.csv")
 
iteration_list = fdsa_close_df.Iteration.tolist()
 
#spsa results to seperate lists
#close
sc_inVehicleTime_est = spsa_close_df.invehicleTime_est.tolist()
sc_accessTime_est = spsa_close_df.accessTime_est.tolist()
sc_egressTime_est = spsa_close_df.egressTime_est.tolist()
sc_transferWalkingTime_est = spsa_close_df.walkingTime_est.tolist()
sc_originWaitTime_est = spsa_close_df.originWaitTime_est.tolist()
sc_transferWaitTime_est = spsa_close_df.transferWaitTime_est.tolist()

#far
sf_inVehicleTime_est = spsa_far_df.invehicleTime_est.tolist()
sf_accessTime_est = spsa_far_df.accessTime_est.tolist()
sf_egressTime_est = spsa_far_df.egressTime_est.tolist()
sf_transferWalkingTime_est = spsa_far_df.walkingTime_est.tolist()
sf_originWaitTime_est = spsa_far_df.originWaitTime_est.tolist()
sf_transferWaitTime_est = spsa_far_df.transferWaitTime_est.tolist()
 
#fdsa results to seperate lists
#close
fc_inVehicleTime_est = fdsa_close_df.invehicleTime_est.tolist()
fc_accessTime_est = fdsa_close_df.accessTime_est.tolist()
fc_egressTime_est = fdsa_close_df.egressTime_est.tolist()
fc_transferWalkingTime_est = fdsa_close_df.walkingTime_est.tolist()
fc_originWaitTime_est = fdsa_close_df.originWaitTime_est.tolist()
fc_transferWaitTime_est = fdsa_close_df.transferWaitTime_est.tolist()

#far
ff_inVehicleTime_est = fdsa_far_df.invehicleTime_est.tolist()
ff_accessTime_est = fdsa_far_df.accessTime_est.tolist()
ff_egressTime_est = fdsa_far_df.egressTime_est.tolist()
ff_transferWalkingTime_est = fdsa_far_df.walkingTime_est.tolist()
ff_originWaitTime_est = fdsa_far_df.originWaitTime_est.tolist()
ff_transferWaitTime_est = fdsa_far_df.transferWaitTime_est.tolist()
 
 
 
#multi line plot to see the change of in vehicle time estimate over the iterations
_prior = list(itertools.repeat(3.0,301))
    

_ = plt.plot(iteration_list, sc_transferWaitTime_est, linestyle = '--', linewidth = 1, color = 'red', label = 'SPSA')
#_ = plt.plot(iteration_list, sf_transferWaitTime_est, linestyle = '--',linewidth = 1, color = 'darkorange', label = 'SPSA far')
_ = plt.plot(iteration_list, fc_transferWaitTime_est, linewidth = 1, color = 'royalblue', label = 'FDSA')
#_ = plt.plot(iteration_list, ff_transferWaitTime_est, linewidth = 1, color = 'seagreen', label = 'FDSA far')

_ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Observed Value')
 
 
_ = plt.xlabel("Iteration")
_ = plt.ylabel('Estimated value the coefficient')
_ = plt.suptitle("Change of Origin Wait Time Coefficient")
#_ = plt.title("Close Estimates", fontsize = 10)
 
_ = plt.legend()
     
#plt.show()
savepath = 'C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\sensitivity_analysis\\17012020 - report to Moeid\\coef_transferWait.svg'
plt.draw()
#plt.show()
plt.savefig(savepath, bbox_inches = 'tight')   



#===============================================================================
#This is to compare FDSA and SPSA
# #load csvs as dataframes
# 
# spsa_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_14\\hp_set14_SPSA_10012020_cleaned.csv")
# fdsa_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_14\\hp_set14_FDSA_10012020_cleaned.csv")
# 
# iteration_list = fdsa_df.Iteration.tolist()
# 
# #spsa results to seperate lists
# 
# s_inVehicleTime_est = spsa_df.invehicleTime_est.tolist()
# s_accessTime_est = spsa_df.accessTime_est.tolist()
# s_egressTime_est = spsa_df.egressTime_est.tolist()
# s_transferWalkingTime_est = spsa_df.walkingTime_est.tolist()
# s_originWaitTime_est = spsa_df.originWaitTime_est.tolist()
# s_transferWaitTime_est = spsa_df.transferWaitTime_est.tolist()
# 
# #fdsa results to seperate lists
# f_inVehicleTime_est = fdsa_df.invehicleTime_est.tolist()
# f_accessTime_est = fdsa_df.accessTime_est.tolist()
# f_egressTime_est = fdsa_df.egressTime_est.tolist()
# t_transferWalkingTime_est = fdsa_df.walkingTime_est.tolist()
# f_originWaitTime_est = fdsa_df.originWaitTime_est.tolist()
# f_transferWaitTime_est = fdsa_df.transferWaitTime_est.tolist()
# 
# 
# 
# #multi line plot to see the change of in vehicle time estimate over the iterations
# _prior = list(itertools.repeat(3.0,301))
#    
# _ = plt.plot(iteration_list, _prior, linestyle = '-.', linewidth = 0.75, color = 'dimgray', label = 'Target')
# _ = plt.plot(iteration_list, f_transferWaitTime_est, linewidth = 1, color = 'royalblue', label = 'FDSA')
# _ = plt.plot(iteration_list, s_transferWaitTime_est, linestyle = '--',linewidth = 1, color = 'red', label = 'SPSA')
# 
# 
# _ = plt.xlabel("Iteration")
# _ = plt.ylabel('Estimated value the coefficient')
# _ = plt.suptitle("Change of Transfer Wait Time Coefficient")
# _ = plt.title("Close Estimates", fontsize = 10)
# 
# _ = plt.legend()
#     
# plt.show()
#===============================================================================

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