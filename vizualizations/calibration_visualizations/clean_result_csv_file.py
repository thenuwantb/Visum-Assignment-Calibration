'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd

load_file  = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_14\\hp_set14_SPSA_10012020.csv"
save_file = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\results\\hyper_parameter_set_14\\hp_set14_SPSA_10012020_cleaned.csv"

resultsdf = pd.read_csv(load_file)
print resultsdf.head()
resultsdf_estimate_list = resultsdf.estimate.tolist()


invehicleTime_est = []
accessTime_est = []
egressTime_est = []
walkingTime_est = []
originWaitTime_est = []
transferWaitTime_est = []

for i in range(len(resultsdf_estimate_list)):
    
    estimate = resultsdf_estimate_list[i]
    
    estimate = estimate.strip("[")
    estimate = estimate.strip("]")
    
    
    estimate_list = estimate.split()
    estimate_list = [float(k) for k in estimate_list]
    
    invehicleTime_est.append(estimate_list[0])
    accessTime_est.append(estimate_list[1])
    egressTime_est.append(estimate_list[2])
    walkingTime_est.append(estimate_list[3])
    originWaitTime_est.append(estimate_list[4])
    transferWaitTime_est.append(estimate_list[5])

#print len(invehicleTime_est)
resultsdf['invehicleTime_est'] = invehicleTime_est
resultsdf['accessTime_est'] = accessTime_est
resultsdf['egressTime_est'] = egressTime_est
resultsdf['walkingTime_est'] = walkingTime_est
resultsdf['originWaitTime_est'] = originWaitTime_est
resultsdf['transferWaitTime_est'] = transferWaitTime_est


resultsdf.to_csv(save_file)