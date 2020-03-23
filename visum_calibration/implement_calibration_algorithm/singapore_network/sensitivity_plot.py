from collections import OrderedDict
from custom_visum_functions.open_close_visum import open_close as ocv
from custom_visum_functions.visum_list_calculations import list_calculations as vlc
from custom_visum_functions.visum_list_calculations import simulated_values_generator_singapore as sgs
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
version_file = "7_HeadwayBased_remove_unwanted_lines_speed_up.ver"
visum_path = os.path.join(path, version_file)
Visum = com.Dispatch("Visum.Visum.170")

ocv.loadVisum(VisumComDispatch=Visum, verPath=visum_path)

observed_stop_point_df = pd.read_csv(
    "E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_stop_data_all_movements_2902200.csv")
observed_line_route_df = pd.read_csv("E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\observed_line_route_data_14032020.csv")
observed_line_route_df["LineName"] = observed_line_route_df["LineName"].astype(str)
observed_line_route_df["Name"] = observed_line_route_df["Name"].astype(str)

# Create dataframe and assign values
df_rmsn_columns = ['in_veh', 'transfer_walk', 'origin_wait', 'transfer_wait', 'transfer_penalty', 'pax_trans_total_rmsn',
                   'pax_trans_walkb_rmsn', 'pax_trans_alightw_rmsn', 'pass_trans_dir_rmsn',
                   'pass_trans_total_combined_rmsn', 'pax_trips_unlinked_rmsn', 'pax_trips_unlinked_0_rmsn',
                   'pax_trips_unlinked_1_rmsn', 'pax_trips_unlinked_2_rmsn', 'pax_trips_unlinked_g_2_rmsn',
                   'paxTripsWoCon']
summary_df = pd.DataFrame(columns=df_rmsn_columns)
coefficient_list = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0]
#coefficient_list = [2.0]
estimate_list = [0.001, 0.001, 0.001, 0.001, 0.001]
#estimate_list = [1, 1, 1, 1, 1]

for estimate in range(len(estimate_list)):
    estimates = copy.copy(estimate_list)

    for i in range(len(coefficient_list)):
        temp_dict = {}
        estimates[estimate] = coefficient_list[i]
        print estimates
        error_dict = sgs.runAssignmentCalculateErrorRMSN_all_error_terms(Visum=Visum, estimateList=estimates, obs_stops_df=observed_stop_point_df, obs_line_routes=observed_line_route_df)

        temp_dict['in_veh'] = estimates[0]
        temp_dict['transfer_walk'] = estimates[1]
        temp_dict['origin_wait'] = estimates[2]
        temp_dict['transfer_wait'] = estimates[3]
        temp_dict['transfer_penalty'] = estimates[4]

        temp_dict['pax_trans_total_rmsn'] = error_dict['pax_trans_total_rmsn']
        temp_dict['pax_trans_walkb_rmsn'] = error_dict['pax_trans_walkb_rmsn']
        temp_dict['pax_trans_alightw_rmsn'] = error_dict['pax_trans_alightw_rmsn']
        temp_dict['pass_trans_dir_rmsn'] = error_dict['pass_trans_dir_rmsn']
        temp_dict['pass_trans_total_combined_rmsn'] = error_dict['pass_trans_total_combined_rmsn']

        temp_dict['pax_trips_unlinked_rmsn'] = error_dict['pax_trips_unlinked_rmsn']
        temp_dict['pax_trips_unlinked_0_rmsn'] = error_dict['pax_trips_unlinked_0_rmsn']
        temp_dict['pax_trips_unlinked_1_rmsn'] = error_dict['pax_trips_unlinked_1_rmsn']
        temp_dict['pax_trips_unlinked_2_rmsn'] = error_dict['pax_trips_unlinked_2_rmsn']
        temp_dict['pax_trips_unlinked_g_2_rmsn'] = error_dict['pax_trips_unlinked_g_2_rmsn']

        temp_dict['paxTripsWoCon'] = error_dict['paxTripsWoCon']
        print error_dict['paxTripsWoCon']

        temp_df = pd.DataFrame(temp_dict, index=[0])
        summary_df = summary_df.append(temp_df)
        temp_dict.clear()

summary_df = summary_df[df_rmsn_columns]
summary_df.to_csv("E:\\Thenuwan\\Singapore_Calibration\\data\\observed\\sensitivity_singapore_network_15032020_all.csv")
