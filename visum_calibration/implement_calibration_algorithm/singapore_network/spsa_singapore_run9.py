'''
Created by : Thenuwan Jayasinghe on 16042020
Notes : In this calibration run, all (inv = 1) the parameters in concern (invehicle<fixed>, transfer walk, origin wait, transfer wait, transfer penalty)
Addition : transfer penalty, seconds will be converted to minutes

***important - all the premeium routes and lines with no time tables removed in '11_HeadwayBased_Headway_cal_changed_remove_prem_bus.ver'. the updated observed values csv file is used
observed_line_route_data_24042020.csv

Values are allowed to change between 1 and 9

The headway calculation method was changed  - with this the unassigned #of trips can be reduced

 2objective functions will be used interchangebly At each iteration, the objective function which provides the highest difference will
be chosen to update the estimates. (implementing the lessons learnt from calibration run 6 and 7)

new additions compared to run 6 and 7 : 1.pax_trans_alightw_rmsn is used seperately, 2. pax_trans_walkb_rmsn,
pass_trans_dir_are combined and considered, 3. PTripsUnlinked0(AP) is used instead on PTripsUnlinked

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
ver_file = "11_HeadwayBased_Headway_cal_changed_remove_prem_bus.ver"
version_path = os.path.join(path, ver_file)
Visum = com.Dispatch("Visum.Visum.170")

# save results
save_result_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_9\\hp_set_13_spsa_24042020_run9.csv"
save_results_all_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_9\\hp_set_13_spsa_all_24042020_run9.csv"

# load visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=version_path)

# read observed data
observed_stop_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_stop_data_all_movements_2902200.csv")
observed_line_route_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_line_route_data_24042020.csv")
observed_line_route_df["LineName"] = observed_line_route_df["LineName"].astype(str)
observed_line_route_df["Name"] = observed_line_route_df["Name"].astype(str)

# saving results from the calibration in a dictionary
results_columns = ['transfer_walk', 'origin_wait', 'transfer_wait', 'transfer_penalty', 'pax_trans_total_rmsn',
                   'pax_trans_walkb_rmsn', 'pax_trans_alightw_rmsn', 'pass_trans_dir_rmsn',
                   'pass_trans_total_combined_rmsn','mean_pax_trans_combined_rmsn', 'pax_trans_walkb_trans_dir_combined_rmsn', 'pax_trips_unlinked_rmsn', 'pax_trips_unlinked_0_rmsn',
                   'pax_trips_unlinked_1_rmsn', 'pax_trips_unlinked_2_rmsn', 'pax_trips_unlinked_g_2_rmsn',
                   'paxTripsWoCon']
results_all_df = pd.DataFrame(columns=results_columns)
results_dict = {}  # may not be used with the new implementation - 10042020

# implement calibration algorithm

max_iterations = 80
# hyper parameter set 13
alpha = 0.602
gamma = 0.101
c = 1.419
a = 4.833
A = 30

objective_function_1 = 'pax_trips_unlinked_0_rmsn'
objective_function_2 = 'pass_trans_total_combined_rmsn'
#objective_function_3 = 'pax_trans_alightw_rmsn'
objective_function_list = [objective_function_1, objective_function_2]

objective_function_count = {objective_function_1: 0, objective_function_2: 0}

# initial guesses

initial_guess = [2.0, 2.0, 2.0, 5.0]  # [in_vehicle=1, transfer_walk, origin_wait, transfer_wait, transfer_penalty]
initial_cost_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=initial_guess,
                                                                        obs_stops_df=observed_stop_df,
                                                                        obs_line_routes=observed_line_route_df)
initial_cost = initial_cost_dict[objective_function_1]
results_all_df = results_all_df.append(sgs.parse_error_from_dict_to_df(initial_cost_dict, initial_guess))

results_dict = {0: [initial_cost, initial_guess]}

current_estimate = np.copy(initial_guess)

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
    cost_increase_list = [cost_increase_dict[objective_function_1], cost_increase_dict[objective_function_2]]

    cost_decrease_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=decrease_u,
                                                                             obs_stops_df=observed_stop_df,
                                                                             obs_line_routes=observed_line_route_df)
    cost_decrease_list = [cost_decrease_dict[objective_function_1], cost_decrease_dict[objective_function_2]]

    # selecting the better objective function for the current iteration, which gives higher gradient
    current_objective_function = sgs.select_better_objective_function(inc_obj_list=cost_increase_list,
                                                                      dec_obj_list=cost_decrease_list,
                                                                      obj_function_list=objective_function_list)
    objective_function_count[current_objective_function] += 1  # to keep a track
    cost_increase = cost_increase_dict[current_objective_function]
    cost_decrease = cost_decrease_dict[current_objective_function]

    # Step 4 - Gradient approximation
    gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
    # print gk

    # Step 5 - Update current_estimate estimate
    previous_estimate = np.copy(current_estimate)

    # --------------fix 05122019---------------------------------
    gk_step_size = ak * gk

    for m in range(len(previous_estimate)):
        if 1.0 <= previous_estimate[m] - gk_step_size[m] <= 9.0:
            current_estimate[m] = previous_estimate[m] - gk_step_size[m]

        else:
            current_estimate[m] = best_estimate[m]

    cost_new_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=current_estimate,
                                                                        obs_stops_df=observed_stop_df,
                                                                        obs_line_routes=observed_line_route_df)

    cost_new = cost_new_dict[objective_function_1]
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

# save all the error terms
results_all_df.to_csv(save_results_all_path)

# Plot
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()

print objective_function_count
