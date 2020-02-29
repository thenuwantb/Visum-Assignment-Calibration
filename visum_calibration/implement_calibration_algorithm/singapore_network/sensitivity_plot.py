from collections import OrderedDict
from custom_visum_functions.open_close_visum import open_close as ocv
from custom_visum_functions.visum_list_calculations import list_calculations as vlc
from custom_visum_functions.visum_list_calculations import simulated_values_generator as sg
from numpy import shape
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import win32com.client as com
import timeit
import copy

# Load visum
path = "E:\\Thenuwan\\Singapore_Calibration"
version_file = "3_HeadwayBased_change_start_time.ver"
visum_path = os.path.join(path, version_file)
Visum = com.Dispatch("Visum.Visum.170")

ocv.loadVisum(VisumComDispatch=Visum, verPath=visum_path)

observed_stop_point_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_stop_data_27022020.csv")

# Create dataframe and assign values
df_rmsn_columns = ['coefficient', 'in_veh', 'tra_walk', 'ori_wait', 'tra_wait']
df_rmsn = pd.DataFrame(columns=df_rmsn_columns)
coefficient_list = (np.arange(1, 6, 1)).tolist()
coefficient_value_series = pd.Series(coefficient_list)
df_rmsn['coefficient'] = coefficient_value_series.values

estimate_list = [1.0, 1.0, 1.0, 1.0]

for estimate in range(len(estimate_list)):
    estimates = copy.copy(estimate_list)

    for i in range(len(coefficient_list)):
        estimates[estimate] = coefficient_list[i]
        print estimates
        rmsn_value = sg.runAssignmentCalculateErrorRMSN_Stops(Visum=Visum, estimateList=estimates, obsStopPoints=observed_stop_point_df)
        print rmsn_value
        df_rmsn.at[i, df_rmsn_columns[estimate + 1]] = rmsn_value

df_rmsn.to_csv("E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\sensitivity_singapore_network_28022020.csv")
