'''
Created by : Thenuwan Jayasinghe on 29.02.2020
Notes : In this calibration run, in-vehicle time will be set to 1 through out the run. As an addition, transfer penalty
        will be calibrated
Addition : transfer penalty, seconds will be converted to minutes
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
ver_file = "5_HeadwayBased_inv_anchored.ver"
version_path = os.path.join(path, ver_file)
Visum = com.Dispatch("Visum.Visum.170")

# save results
save_result_path = "E:\\Thenuwan\\Singapore_Calibration\\data\\results\\run_2\\hp_set_13_spsa_07032020.csv"

# load visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=version_path)

# read observed data
observed_stop_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_stop_data_all_movements_2902200.csv")

# implement calibration algorithm

max_iterations = 3
# hyper parameter set 13
alpha = 0.602
gamma = 0.101
c = 1.419
a = 4.833
A = 30

initial_guess = [1.0, 1.0, 1.0, 5.0]
#initial_cost = sgs.run_assignment_calculate_error_stops_pax_trans_combined_2(visum=Visum, estimate_list=initial_guess, obs_stops_df=observed_stop_df)
initial_cost = 7.61633661217
#print initial_guess, initial_cost

plot_dict = OrderedDict()
plot_dict = {0: [initial_cost, initial_guess]}

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
        if 0.0001 < current_estimate[i] + ck * deltaK[i] <= 6.0:
            # current_estimate[i] + ck * deltaK[i] > 0 and current_estimate[i] + ck * deltaK[i] <= 9.9
            increase_u[i] = current_estimate[i] + ck * deltaK[i]
        else:
            increase_u[i] = current_estimate[i]

    for j in range(len(decrease_u)):
        if 0.0001 < current_estimate[j] - ck * deltaK[j] <= 6.0:
            decrease_u[j] = current_estimate[j] - ck * deltaK[j]
        else:
            decrease_u[j] = current_estimate[j]

    # Step 3 - Function evaluation
    cost_increase = sgs.run_assignment_calculate_error_stops_pax_trans_combined_2(visum=Visum, estimate_list=increase_u,
                                                                                  obs_stops_df=observed_stop_df)
    cost_decrease = sgs.run_assignment_calculate_error_stops_pax_trans_combined_2(visum=Visum, estimate_list=decrease_u,
                                                                                  obs_stops_df=observed_stop_df)

    # Step 4 - Gradient approximation
    gk = np.dot((cost_increase - cost_decrease) / (2.0 * ck), deltaK)
    # print gk

    # Step 5 - Update current_estimate estimate
    previous_estimate = np.copy(current_estimate)

    # --------------fix 05122019---------------------------------
    gk_step_size = ak * gk

    for m in range(len(previous_estimate)):
        if 0 <= previous_estimate[m] - gk_step_size[m] <= 6.0:
            current_estimate[m] = previous_estimate[m] - gk_step_size[m]

        else:
            current_estimate[m] = best_estimate[m]

    cost_new = sgs.run_assignment_calculate_error_stops_pax_trans_combined_2(visum=Visum,
                                                                             estimate_list=current_estimate,
                                                                             obs_stops_df=observed_stop_df)
    # --------------fix 05122019---------------------------------

    if cost_new < best_rmsn:
        best_rmsn = cost_new
        best_estimate = np.copy(current_estimate)

    print k
    print cost_new
    print current_estimate
    print best_estimate

    estimate_to_dict = np.copy(current_estimate)

    plot_dict[k + 1] = [cost_new, estimate_to_dict]

t_duration = timeit.default_timer() - t_start
print "Duration = " + str(t_duration)

# saving values to a Data Frame
results_df = pd.DataFrame()

# Creation of the plot - and then save the values to a Data Frame  - change made on 10122019
iteration_id = []
cost_value = []
estimate_list = []
for key, value in plot_dict.items():
    iteration_id.append(key)
    cost_value.append(value[0])
    estimate_list.append(value[1])

results_df['Iteration'] = iteration_id
results_df['RMSN'] = cost_value
results_df['estimate'] = estimate_list

results_df.to_csv(save_result_path)

# Plot
plt.plot(iteration_id, cost_value)
plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.show()
