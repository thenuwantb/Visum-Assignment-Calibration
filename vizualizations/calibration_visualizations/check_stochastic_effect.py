'''
Created on 18 Dec 2019

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt

# load all files related to FDSA from the results of 18122019

fdsa_df_1 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\fdsa_far_hp_set_2_run_1.csv")
fdsa_df_2 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\fdsa_far_hp_set_2_run_2.csv")
fdsa_df_3 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\fdsa_far_hp_set_2_run_3.csv")
fdsa_df_4 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\fdsa_far_hp_set_2_run_4.csv")

fdsa_rmsn_1 = fdsa_df_1.RMSN.tolist()
fdsa_rmsn_2 = fdsa_df_2.RMSN.tolist()
fdsa_rmsn_3 = fdsa_df_3.RMSN.tolist()
fdsa_rmsn_4 = fdsa_df_4.RMSN.tolist()

iterations_list = fdsa_df_1.Iteration.tolist()

_ = plt.plot(iterations_list, fdsa_rmsn_1, linestyle='-', color='royalblue', label='FDSA')
_ = plt.plot(iterations_list, fdsa_rmsn_2, linestyle='--', color='royalblue', label='FDSA')
_ = plt.plot(iterations_list, fdsa_rmsn_3, linestyle='-.', color='royalblue', label='FDSA')
_ = plt.plot(iterations_list, fdsa_rmsn_4, linestyle=':', color='royalblue', label='FDSA')

# load all files related to FDSA from the results of 18122019

spsa_df_1 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\spsa_far_hp_set_2_run_1.csv")
spsa_df_2 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\spsa_far_hp_set_2_run_2.csv")
spsa_df_3 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\spsa_far_hp_set_2_run_3.csv")
spsa_df_4 = pd.read_csv(
    "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\18122019\\results\\spsa_far_hp_set_2_run_4.csv")

spsa_rmsn_1 = spsa_df_1.RMSN.tolist()
spsa_rmsn_2 = spsa_df_2.RMSN.tolist()
spsa_rmsn_3 = spsa_df_3.RMSN.tolist()
spsa_rmsn_4 = spsa_df_4.RMSN.tolist()

iterations_list = spsa_df_1.Iteration.tolist()

_ = plt.plot(iterations_list, spsa_rmsn_1, linestyle='-', color='red', label='SPSA')  # marker = '^'
_ = plt.plot(iterations_list, spsa_rmsn_2, linestyle='--', color='red', label='SPSA')
_ = plt.plot(iterations_list, spsa_rmsn_3, linestyle='-.', color='red', label='SPSA')
_ = plt.plot(iterations_list, spsa_rmsn_4, linestyle=':', color='red', label='SPSA')

plt.xlabel("Number of Iterations")
plt.ylabel("RMSN")

plt.legend()
plt.show()
