'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt

spsa_df_1  = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\different_rand_num_spsa\\spsa_far_hp_set_2_run_1_rs_100.csv")
spsa_df_2  = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\different_rand_num_spsa\\spsa_far_hp_set_2_run_2_rs_159.csv")
spsa_df_3  = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\different_rand_num_spsa\\spsa_far_hp_set_2_run_3_rs_486.csv")
spsa_df_4  = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\different_rand_num_spsa\\spsa_far_hp_set_2_run_4_rs_999.csv")

spsa_rmsn_1 = spsa_df_1.RMSN.tolist()
spsa_rmsn_2 = spsa_df_2.RMSN.tolist()
spsa_rmsn_3 = spsa_df_3.RMSN.tolist()
spsa_rmsn_4 = spsa_df_4.RMSN.tolist()

iterations_list = spsa_df_1.Iteration.tolist()

_ = plt.plot(iterations_list, spsa_rmsn_1, color = 'forestgreen', label = 'Rand 100', alpha = 0.8) #marker = '^'
_ = plt.plot(iterations_list, spsa_rmsn_2, color = 'orangered', label = 'Rand 159', alpha = 0.8)
_ = plt.plot(iterations_list, spsa_rmsn_3, color = 'blueviolet', label = 'Rand 486', alpha = 0.8)
_ = plt.plot(iterations_list, spsa_rmsn_4, color = 'cornflowerblue', label = 'Rand 999', alpha = 0.8)

plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")
plt.legend()

plt.show()