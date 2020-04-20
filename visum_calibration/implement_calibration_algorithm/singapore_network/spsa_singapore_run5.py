'''
Created by : Thenuwan Jayasinghe on 08042020
Notes : In this calibration run, all the parameters in concern (invehicle = 1, transfer walk, origin wait, transfer wait, transfer penalty)
Addition : transfer penalty, seconds will be converted to minutes
The headway calculation method was changed  - with this the unassigned #of trips is reduce

Objective function calucation is changed to trips made on line routes with one transfer
At the same time, objective function value of other potential objective functions will be captured and saved: This will
later help to understand the 1. Quality of the solution, 2. Other potential objective functions
'''

from collections import OrderedDict
from custom_visum_functions.open_close_visum import open_close as ocv
from custom_visum_functions.visum_list_calculations import list_calculations_singapore as vlcs
from custom_visum_functions.visum_list_calculations import simulated_values_generator_singapore as sgs
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import win32com.client as com
import timeit

# Load Visum Version and create a Network Object
path = "E:\\Thenuwan\\Singapore_Calibration"
ver_file = "10_HeadwayBased_Headway_cal_changed.ver"
version_path = os.path.join(path, ver_file)
Visum = com.Dispatch("Visum.Visum.170")

# save results
save_result_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_5\\hp_set_13_spsa_11042020_run5.csv"
save_results_all_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_5\\hp_set_13_spsa_all_042020_run5.csv"

# load visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=version_path)

# read observed data
observed_stop_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_stop_data_all_movements_2902200.csv")
observed_line_route_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_line_route_data_14032020.csv")
observed_line_route_df["LineName"] = observed_line_route_df["LineName"].astype(str)
observed_line_route_df["Name"] = observed_line_route_df["Name"].astype(str)

#saving results from the calibration in a dictionary
results_columns = ['transfer_walk', 'origin_wait', 'transfer_wait', 'transfer_penalty', 'pax_trans_total_rmsn',
                   'pax_trans_walkb_rmsn', 'pax_trans_alightw_rmsn', 'pass_trans_dir_rmsn',
                   'pass_trans_total_combined_rmsn', 'pax_trips_unlinked_rmsn', 'pax_trips_unlinked_0_rmsn',
                   'pax_trips_unlinked_1_rmsn', 'pax_trips_unlinked_2_rmsn', 'pax_trips_unlinked_g_2_rmsn',
                   'paxTripsWoCon']
results_all_df = pd.DataFrame(columns=results_columns)
results_dict = {} #may not be used with the new implementation - 10042020

# implement calibration algorithm

max_iterations = 80
# hyper parameter set 13
alpha = 0.602
gamma = 0.101
c = 1.419
a = 4.833
A = 30

objective_function = 'pax_trips_unlinked_0_rmsn'

#initial guesses

initial_guess = [2.0, 2.0, 2.0, 5.0] #[transfer_walk, origin_wait, transfer_wait, transfer_penalty]
initial_cost_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=initial_guess,
                                                                        obs_stops_df=observed_stop_df,
                                                                        obs_line_routes=observed_line_route_df)
initial_cost = initial_cost_dict[objective_function]
results_all_df = results_all_df.append(sgs.parse_error_from_dict_to_df(initial_cost_dict, initial_guess))


results_dict = {0: [initial_cost, initial_guess]}

current_estimate = np.copy(initial_guess)
best_estimate = np.copy(initial_guess)
best_rmsn = np.copy(initial_cost)

np.random.seed(55)

# measure time - start

t_start = timeit.default_timer()

for k in range(max_iterations):

    ak = a / (A + k + 1) ** alpha
    ck = c / (k + 1) ** gamma

    # Step 2 - Generation of simultaneous perturbation vector

    deltaK = np.random.choice([-1, 1], size=len(current_estimate), p=[0.5, 0.5])  # delta_k = np.array([1,-1])

    # looping over each element and check whether it is in range (0,9) after the change
    increase_u = np.copy(current_estimate)
    decrease_u = np.copy(current_estimate)

    for i in range(len(increase_u)):
        if 1.0 < current_estimate[i] + ck * deltaK[i] <= 9.0:
            # current_estimate[i] + ck * deltaK[i] > 0 and current_estimate[i] + ck * deltaK[i] <= 9.9
            increase_u[i] = current_estimate[i] + ck * deltaK[i]
        else:
            increase_u[i] = current_estimate[i]

    for j in range(len(decrease_u)):
        if 1.0 < current_estimate[j] - ck * deltaK[j] <= 9.0:
            decrease_u[j] = current_estimate[j] - ck * deltaK[j]
        else:
            decrease_u[j] = current_estimate[j]

    # Step 3 - Function evaluation
    cost_increase_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=increase_u,
                                                                            obs_stops_df=observed_stop_df,
                                                                            obs_line_routes=observed_line_route_df)
    cost_increase = cost_increase_dict[objective_function]

    cost_decrease_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=decrease_u,
                                                                             obs_stops_df=observed_stop_df,
                                                                             obs_line_routes=observed_line_route_df)
    cost_decrease = cost_decrease_dict[objective_function]


    # Step 4 - Gradient approximation
    gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
    # print gk

    # Step 5 - Update current_estimate estimate
    previous_estimate = np.copy(current_estimate)

    # --------------fix 05122019---------------------------------
    gk_step_size = ak * gk

    for m in range(len(previous_estimate)):
        if 0 <= previous_estimate[m] - gk_step_size[m] <= 9.0:
            current_estimate[m] = previous_estimate[m] - gk_step_size[m]

        else:
            current_estimate[m] = best_estimate[m]

    cost_new_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=current_estimate,
                                                                             obs_stops_df=observed_stop_df,
                                                                             obs_line_routes=observed_line_route_df)

    cost_new = cost_new_dict[objective_function]
    results_all_df = results_all_df.append(sgs.parse_error_from_dict_to_df(cost_new_dict, current_estimate))
    # --------------fix 05122019---------------------------------

    if cost_new < best_rmsn:
        best_rmsn = cost_new
        best_estimate = np.copy(current_estimate)

    print k
    print cost_new
    print current_estimate
    print best_estimate

    estimate_to_dict = np.copy(current_estimate)

    results_dict[k + 1] = [cost_new, estimate_to_dict]

t_duration = timeit.default_timer() - t_start
print "Duration = " + str(t_duration)

# saving values to a Data Frame
results_df_prev = pd.DataFrame()

# Creation of the plot - and then save the values to a Data Frame  - change made on 10122019
iteration_id = []
cost_value = []
estimate_list = []
for key, value in results_dict.items():
    iteration_id.append(key)
    cost_value.append(value[0])
    estimate_list.append(value[1])

results_df_prev['Iteration'] = iteration_id
results_df_prev['RMSN'] = cost_value
results_df_prev['estimate'] = estimate_list

results_df_prev.to_csv(save_result_path)

#save all the error terms
results_all_df.to_csv(save_results_all_path)

# Plot
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()
