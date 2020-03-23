'''
Created on 20 Mar 2020

@author: thenuwan.jayasinghe
'''

import pandas as pd
import matplotlib.pyplot as plt

plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)

coefficients_run_1 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_1\\cleaned_run_1_rmsn_hp_set_13_spsa_29022020.csv")
coefficients_run_2 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_2\\cleaned_run_2_rmsn_hp_set_13_spsa_07032020.csv")
coefficients_run_3 = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_3\\cleaned_run_3_rmsn_hp_set_13_spsa_11032020.csv")
coefficients_run_1 = coefficients_run_1.iloc[0:81]

row_id_min_rmsn_run1 = coefficients_run_1[["RMSN"]].idxmin().item()
row_id_min_rmsn_run2 = coefficients_run_2[["RMSN"]].idxmin().item()
row_id_min_rmsn_run3 = coefficients_run_3[["RMSN"]].idxmin().item()

min_rmsn_run1 = round(coefficients_run_1['RMSN'].min(),3)
min_rmsn_run2 = round(coefficients_run_2['RMSN'].min(),3)
min_rmsn_run3 = round(coefficients_run_3['RMSN'].min(),3)


#run_1 coefficients to a list
run_1_inv_time = coefficients_run_1['in_vehicle_time_est'].tolist()
run_1_transfer_walk_time = coefficients_run_1['transfer_walk_time_est'].tolist()
run_1_origin_wait_time = coefficients_run_1['origin_wait_time_est'].tolist()
run_1_transfer_wait_time = coefficients_run_1['transfer_wait_time_est'].tolist()

#run_2 coefficients to a list
run_2_transfer_walk_time = coefficients_run_2['transfer_walk_time_est'].tolist()
run_2_origin_wait_time = coefficients_run_2['origin_wait_time_est'].tolist()
run_2_transfer_wait_time = coefficients_run_2['transfer_wait_time_est'].tolist()
run_2_transfer_penalty = coefficients_run_2['transfer_penalty_min_est'].tolist()

#run_2 coefficients to a list
run_3_inv_time = coefficients_run_3['in_vehicle_time_est'].tolist()
run_3_transfer_walk_time = coefficients_run_3['transfer_walk_time_est'].tolist()
run_3_origin_wait_time = coefficients_run_3['origin_wait_time_est'].tolist()
run_3_transfer_wait_time = coefficients_run_3['transfer_wait_time_est'].tolist()
run_3_transfer_penalty = coefficients_run_3['transfer_penalty_min_est'].tolist()

iteration_list = coefficients_run_2.Iteration.tolist()

#compare change of in-vehicle time coefficient estimate
fig1, ax1 = plt.subplots()
ax1.plot(iteration_list, run_1_inv_time, label = 'Transfer penalty = 5min', color = 'blue', alpha=0.7, linestyle='-.')
ax1.plot(iteration_list[row_id_min_rmsn_run1], run_1_inv_time[row_id_min_rmsn_run1], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='blue')
ax1.text(iteration_list[row_id_min_rmsn_run1]-5, run_1_inv_time[row_id_min_rmsn_run1]+0.2, "$RMSN_{min}$ =" + str(min_rmsn_run1))

ax1.plot(iteration_list, run_3_inv_time, label = 'All parameters', color = 'green', alpha=0.7, linestyle='-.')
ax1.plot(iteration_list[row_id_min_rmsn_run3], run_3_inv_time[row_id_min_rmsn_run3], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='green')
ax1.text(iteration_list[row_id_min_rmsn_run3]-5, run_3_inv_time[row_id_min_rmsn_run3]+0.3, "$RMSN_{min}$ =" + str(min_rmsn_run3))

ax1.set_xlabel("Iteration")
ax1.set_ylabel("Estimate of the coefficient")

plt.legend()

plt.show()

#compare change of transfer_walk_time time coefficient estimate
fig2, ax2 = plt.subplots()
ax2.plot(iteration_list, run_1_transfer_walk_time, label = 'Transfer penalty = 5min', color = 'blue', alpha=0.7, linestyle='-.')
ax2.plot(iteration_list[row_id_min_rmsn_run1], run_1_transfer_walk_time[row_id_min_rmsn_run1], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='blue')
ax2.text(iteration_list[row_id_min_rmsn_run1]-2, run_1_transfer_walk_time[row_id_min_rmsn_run1]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run1))

ax2.plot(iteration_list, run_3_transfer_walk_time, label = 'All parameters', color = 'green', alpha=0.7, linestyle='-.')
ax2.plot(iteration_list[row_id_min_rmsn_run3], run_3_transfer_walk_time[row_id_min_rmsn_run3], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='green')
ax2.text(iteration_list[row_id_min_rmsn_run3]-3, run_3_transfer_walk_time[row_id_min_rmsn_run3]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run3))

ax2.plot(iteration_list, run_2_transfer_walk_time, label = 'In-vehicle = 1', color = 'red', alpha=0.7,)
ax2.plot(iteration_list[row_id_min_rmsn_run2], run_2_transfer_walk_time[row_id_min_rmsn_run2], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='red')
ax2.text(iteration_list[row_id_min_rmsn_run2]-3, run_2_transfer_walk_time[row_id_min_rmsn_run2]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run2))

ax2.set_xlabel("Iteration")
ax2.set_ylabel("Estimate of the coefficient")

plt.legend()

plt.show()

#compare change of origin_wait_time time coefficient estimate
fig3, ax3 = plt.subplots()
ax3.plot(iteration_list, run_1_origin_wait_time, label = 'Transfer penalty = 5min', color = 'blue', alpha=0.7, linestyle='-.')
ax3.plot(iteration_list[row_id_min_rmsn_run1], run_1_origin_wait_time[row_id_min_rmsn_run1], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='blue')
ax3.text(iteration_list[row_id_min_rmsn_run1]-2, run_1_origin_wait_time[row_id_min_rmsn_run1]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run1))

ax3.plot(iteration_list, run_3_origin_wait_time, label = 'All parameters', color = 'green', alpha=0.7, linestyle='-.')
ax3.plot(iteration_list[row_id_min_rmsn_run3], run_3_origin_wait_time[row_id_min_rmsn_run3], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='green')
ax3.text(iteration_list[row_id_min_rmsn_run3]-3, run_3_origin_wait_time[row_id_min_rmsn_run3]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run3))

ax3.plot(iteration_list, run_2_origin_wait_time, label = 'In-vehicle = 1', color = 'red', alpha=0.7,)
ax3.plot(iteration_list[row_id_min_rmsn_run2], run_2_origin_wait_time[row_id_min_rmsn_run2], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='red')
ax3.text(iteration_list[row_id_min_rmsn_run2]-3, run_2_origin_wait_time[row_id_min_rmsn_run2]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run2))

ax3.set_xlabel("Iteration")
ax3.set_ylabel("Estimate of the coefficient")

plt.legend()

plt.show()

#compare change of transfer_wait_time coefficient estimate

fig4, ax4 = plt.subplots()
ax4.plot(iteration_list, run_1_transfer_wait_time, label = 'Transfer penalty = 5min', color = 'blue', alpha=0.7, linestyle='-.')
ax4.plot(iteration_list[row_id_min_rmsn_run1], run_1_transfer_wait_time[row_id_min_rmsn_run1], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='blue')
ax4.text(iteration_list[row_id_min_rmsn_run1]-2, run_1_transfer_wait_time[row_id_min_rmsn_run1]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run1))

ax4.plot(iteration_list, run_3_transfer_wait_time, label = 'All parameters', color = 'green', alpha=0.7, linestyle='-.')
ax4.plot(iteration_list[row_id_min_rmsn_run3], run_3_transfer_wait_time[row_id_min_rmsn_run3], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='green')
ax4.text(iteration_list[row_id_min_rmsn_run3]-3, run_3_transfer_wait_time[row_id_min_rmsn_run3]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run3))

ax4.plot(iteration_list, run_2_transfer_wait_time, label = 'In-vehicle = 1', color = 'red', alpha=0.7,)
ax4.plot(iteration_list[row_id_min_rmsn_run2], run_2_transfer_wait_time[row_id_min_rmsn_run2], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='red')
ax4.text(iteration_list[row_id_min_rmsn_run2]-3, run_2_transfer_wait_time[row_id_min_rmsn_run2]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run2))

ax4.set_xlabel("Iteration")
ax4.set_ylabel("Estimate of the coefficient")

plt.legend()

plt.show()

#compare change of transfer penalty values estimate

fig5, ax5 = plt.subplots()

ax5.plot(iteration_list, run_3_transfer_penalty, label = 'All parameters', color = 'green', alpha=0.7, linestyle='-.')
ax5.plot(iteration_list[row_id_min_rmsn_run3], run_3_transfer_penalty[row_id_min_rmsn_run3], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='green')
ax5.text(iteration_list[row_id_min_rmsn_run3]-3, run_3_transfer_penalty[row_id_min_rmsn_run3]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run3))

ax5.plot(iteration_list, run_2_transfer_penalty, label = 'In-vehicle = 1', color = 'red', alpha=0.7,)
ax5.plot(iteration_list[row_id_min_rmsn_run2], run_2_transfer_penalty[row_id_min_rmsn_run2], 
         marker='s', color = 'none',markerfacecolor='none', markersize=18,
         markeredgecolor='red')
ax5.text(iteration_list[row_id_min_rmsn_run2]-3, run_2_transfer_penalty[row_id_min_rmsn_run2]-0.3, "$RMSN_{min}$ =" + str(min_rmsn_run2))

ax5.set_xlabel("Iteration")
ax5.set_ylabel("Estimate of the coefficient")

plt.legend()

plt.show()