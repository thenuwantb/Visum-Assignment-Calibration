'''
Use MAPE error as the loss function. Use passenger transfers at stops to calculate the error
15072020 Then switch to spsa-dof and try to reduce all 3 error terms

Initial guess : Same as the thesis
first 10 - reduce total transfers mape
next 15 - dof-rmsn
last 5 - reduce total transfers mape
ck_manipulation list [1,1,1,1]

'''

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
# ver_file = "11_Remove_premium_0.0475_mean_headway_28042020.ver"
ver_file = "11.2_Remove_premium_0.01_mean_head_way_27042020.ver"
version_path = os.path.join(path, ver_file)
Visum = com.Dispatch("Visum.Visum.170")

# save results
save_result_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_17\\hp_set_13_spsa_21072020_run17_calibrated_model.csv"
save_results_all_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_17\\hp_set_13_spsa_all_21072020_run17_calibrated_model.csv"

# load visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=version_path)

# read observed data
observed_stop_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_stop_data_all_movements_total_transfers_g_5000_07102020.csv")
observed_line_route_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_line_route_data_24042020.csv")
observed_line_route_df["LineName"] = observed_line_route_df["LineName"].astype(str)
observed_line_route_df["Name"] = observed_line_route_df["Name"].astype(str)

# saving results from the calibration in a dictionary

results_columns = ['objective_function',

                   'pax_trans_total_rmsn',
                   'pax_trans_total_rmsn_0',
                   'pax_trans_total_mape',

                   'pax_trans_walkb_rmsn',
                   'pax_trans_walkb_rmsn_0',
                   'pax_trans_walkb_mape',

                   'pax_trans_alightw_rmsn',
                   'pax_trans_alightw_rmsn_0',
                   'pax_trans_alightw_mape',

                   'pax_trans_dir_rmsn',
                   'pax_trans_dir_rmsn_0'
                   'pax_trans_dir_mape',

                   'pax_trans_total_combined_rmsn',
                   'pax_trans_total_combined_rmsn_0',
                   'pax_trans_total_combined_mape',

                   'mean_pax_trans_combined_rmsn',
                   'pax_trans_walkb_trans_dir_combined_rmsn',

                   'pax_trips_unlinked_rmsn',
                   'pax_trips_unlinked_rmsn_0',
                   'pax_trips_unlinked_mape',

                   'pax_trips_unlinked_0_rmsn',
                   'pax_trips_unlinked_0_rmsn_0',
                   'pax_trips_unlinked_0_mape'

                   'pax_trips_unlinked_1_rmsn',
                   'pax_trips_unlinked_1_rmsn_0',
                   'pax_trips_unlinked_1_mape',

                   'pax_trips_unlinked_2_rmsn',
                   'pax_trips_unlinked_2_rmsn_0'
                   'pax_trips_unlinked_2_mape',

                   'pax_trips_unlinked_g_2_rmsn',
                   'pax_trips_unlinked_g_2_rmsn_0'
                   'pax_trips_unlinked_g_2_mape',

                   'transfer_walk',
                   'origin_wait',
                   'transfer_wait',
                   'transfer_penalty',
                   'paxTripsWoCon']

results_all_df = pd.DataFrame(columns=results_columns)
results_dict = {}  # may not be used with the new implementation - 10042020

# implement calibration algorithm

max_iterations = 30
# hyper parameter set 13
alpha = 0.602
gamma = 0.101
c = 1.419
a = 4.833
A = 30

objective_function_1 = 'pax_trans_total_mape'
objective_function_s_1 = 'pax_trips_unlinked_0_rmsn'
objective_function_s_2 = 'pax_trans_total_rmsn'  # s = switching

objective_function_switch_list = [objective_function_s_1, objective_function_s_2]

# initial guesses
# initial_guess = [2.0, 2.0, 2.0, 5.0]  # [in_vehicle=1, transfer_walk, origin_wait, transfer_wait, transfer_penalty]
initial_guess = [2.00, 2.00, 2.00, 5.00]
best_estimate = np.copy(initial_guess)

ck_manipulate = [1.00, 1.00, 1.00, 1.00]
initial_cost_dict = sgs.runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum=Visum, estimateList=initial_guess,
                                                                              obs_stops_df=observed_stop_df,
                                                                              obs_line_routes=observed_line_route_df)
initial_cost = initial_cost_dict[objective_function_1]
results_all_df = results_all_df.append(
    sgs.parse_error_from_dict_to_df(simulated_error_dict=initial_cost_dict, current_estimate=initial_guess,
                                    objective_function=objective_function_1))

results_dict = {0: [initial_cost, initial_guess]}

current_estimate = np.copy(initial_guess)

best_rmsn = np.copy(initial_cost)  # lowest mape is selected at best estimate

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
        if 1.0 < current_estimate[i] + ck * ck_manipulate[i] * deltaK[i] <= 9.0:
            # current_estimate[i] + ck * deltaK[i] > 0 and current_estimate[i] + ck * deltaK[i] <= 9.9
            increase_u[i] = current_estimate[i] + ck * ck_manipulate[i] * deltaK[i]
        else:
            increase_u[i] = current_estimate[i]

    for j in range(len(decrease_u)):
        if 1.0 < current_estimate[j] - ck * ck_manipulate[j] * deltaK[j] <= 9.0:
            decrease_u[j] = current_estimate[j] - ck * ck_manipulate[j] * deltaK[j]
        else:
            decrease_u[j] = current_estimate[j]

    # Step 3 - Function evaluation
    cost_increase_dict = sgs.runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum=Visum, estimateList=increase_u,
                                                                                   obs_stops_df=observed_stop_df,
                                                                                   obs_line_routes=observed_line_route_df)

    cost_decrease_dict = sgs.runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum=Visum, estimateList=decrease_u,
                                                                                   obs_stops_df=observed_stop_df,
                                                                                   obs_line_routes=observed_line_route_df)

    if k < 10:

        # current_objective_function = objective_function_1

        # objective_function_count[current_objective_function] += 1  # to keep a track
        cost_increase = cost_increase_dict[objective_function_1]
        cost_decrease = cost_decrease_dict[objective_function_1]

        # Step 4 - Gradient approximation
        gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
        gk_step_size = ak * gk

        # Step 5 - Update current_estimate estimate
        previous_estimate = np.copy(current_estimate)

        for m in range(len(previous_estimate)):
            if 1.0 <= previous_estimate[m] - gk_step_size[m] <= 9.0:
                current_estimate[m] = previous_estimate[m] - gk_step_size[m]

            else:
                current_estimate[m] = best_estimate[m]

        cost_new_dict = sgs.runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum=Visum,
                                                                                  estimateList=current_estimate,
                                                                                  obs_stops_df=observed_stop_df,
                                                                                  obs_line_routes=observed_line_route_df)

        cost_new = cost_new_dict[objective_function_1]
        results_all_df = results_all_df.append(
            sgs.parse_error_from_dict_to_df(simulated_error_dict=cost_new_dict, current_estimate=current_estimate,
                                            objective_function=objective_function_1))
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

    elif 10 <= k <= 25:
        cost_increase_list = [cost_increase_dict[objective_function_s_1], cost_increase_dict[objective_function_s_2]]
        cost_decrease_list = [cost_decrease_dict[objective_function_s_1], cost_decrease_dict[objective_function_s_2]]

        current_objective_function = sgs.select_better_objective_function(inc_obj_list=cost_increase_list,
                                                                          dec_obj_list=cost_decrease_list,
                                                                          obj_function_list=objective_function_switch_list)

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

        cost_new_dict = sgs.runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum=Visum,
                                                                                  estimateList=current_estimate,
                                                                                  obs_stops_df=observed_stop_df,
                                                                                  obs_line_routes=observed_line_route_df)

        cost_new = cost_new_dict[objective_function_1]
        results_all_df = results_all_df.append(
            sgs.parse_error_from_dict_to_df(simulated_error_dict=cost_new_dict, current_estimate=current_estimate,
                                            objective_function=current_objective_function))

        if cost_new < best_rmsn:
            best_rmsn = cost_new
            best_estimate = np.copy(current_estimate)

        print k
        print cost_new
        print current_estimate
        print best_estimate

        estimate_to_dict = np.copy(current_estimate)

        results_dict[k + 1] = [cost_new, estimate_to_dict]

    else:

        # current_objective_function = objective_function_1

        # objective_function_count[current_objective_function] += 1  # to keep a track
        cost_increase = cost_increase_dict[objective_function_1]
        cost_decrease = cost_decrease_dict[objective_function_1]

        # Step 4 - Gradient approximation
        gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
        gk_step_size = ak * gk

        # Step 5 - Update current_estimate estimate
        previous_estimate = np.copy(current_estimate)

        for m in range(len(previous_estimate)):
            if 1.0 <= previous_estimate[m] - gk_step_size[m] <= 9.0:
                current_estimate[m] = previous_estimate[m] - gk_step_size[m]

            else:
                current_estimate[m] = best_estimate[m]

        cost_new_dict = sgs.runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum=Visum,
                                                                                  estimateList=current_estimate,
                                                                                  obs_stops_df=observed_stop_df,
                                                                                  obs_line_routes=observed_line_route_df)

        cost_new = cost_new_dict[objective_function_1]
        results_all_df = results_all_df.append(
            sgs.parse_error_from_dict_to_df(simulated_error_dict=cost_new_dict, current_estimate=current_estimate,
                                            objective_function=objective_function_1))
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
