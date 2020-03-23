'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd

load_file = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_3\\run_3_rmsn_hp_set_13_spsa_11032020.csv"
save_file = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_3\\cleaned_run_3_rmsn_hp_set_13_spsa_11032020.csv"

resultsdf = pd.read_csv(load_file)
print resultsdf.head()
resultsdf_estimate_list = resultsdf.estimate.tolist()

#access_time_est = []
#egress_time_est = []
inv_time_est = []
transfer_walk_time_est = []
origin_wait_time_est = []
transfer_wait_time_est = []
transfer_penalty_est = []

for i in range(len(resultsdf_estimate_list)):
    estimate = resultsdf_estimate_list[i]

    estimate = estimate.strip("[")
    estimate = estimate.strip("]")

    estimate_list = estimate.split()
    print estimate_list
    estimate_list = [float(k) for k in estimate_list]
    
    inv_time_est.append(estimate_list[0])
    transfer_walk_time_est.append(estimate_list[1])
    origin_wait_time_est.append(estimate_list[2])
    transfer_wait_time_est.append(estimate_list[3])
    transfer_penalty_est.append(estimate_list[4])

# print len(invehicleTime_est)
resultsdf['in_vehicle_time_est'] = inv_time_est
resultsdf['transfer_walk_time_est'] = transfer_walk_time_est
resultsdf['origin_wait_time_est'] = origin_wait_time_est
resultsdf['transfer_wait_time_est'] = transfer_wait_time_est
resultsdf['transfer_penalty_min_est'] = transfer_penalty_est

resultsdf.to_csv(save_file)
