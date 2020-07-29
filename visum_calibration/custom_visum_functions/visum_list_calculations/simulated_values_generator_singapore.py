'''
Created on 14 Jan 2020

@author: thenuwan.jayasinghe
'''
import custom_visum_functions.visum_list_calculations.list_calculations_singapore as vlcs
import custom_visum_functions.satistical_calculations.error_calculations as ec
import pandas as pd
import numpy as np


# Calculate rmsn error
def run_assignment_calculate_error_stops_pax_trans_total(visum, estimate_list, obs_stops_df):
    """
    Calculates the error for PassTransTotal(AP)
    :param visum: Visum object
    :param estimate_list: A list, which contains the estimates in order [in_vehicle,
    transfer_walk, origin_wait, transfer_wait] note : transfer penalty can also be added - not implemented yet
    :param obs_stops_df: pandas data rame with the observed values of a stop.
     :return: scalar error value
    """
    set_impedence_values_run_assignment(visum, estimate_list)
    sim_stops = simulate_stop_ap_volumes(visum)
    stops_merged = obs_stops_df.merge(sim_stops, on="No")

    pax_trans_total_obs = stops_merged['PassTransTotal(AP)_Obs'].tolist()
    pax_trans_total_sim = stops_merged['PassTransTotal(AP)_Sim'].tolist()

    pass_trans_total_rmsn = ec.calculate_rmsn(pax_trans_total_obs, pax_trans_total_sim)

    return pass_trans_total_rmsn


def run_assignment_calculate_error_stops_pax_trans_combined(visum, estimate_list, obs_stops_df):
    """
    Calculates the error for PassTransWalkBoard(AP), PassTransAlightWalk(AP), PassTransDir(AP) in one list
    :param visum: Visum object
    :param estimate_list: A list, which contains the estimates in order [in_vehicle,
    transfer_walk, origin_wait, transfer_wait] note : transfer penalty can also be added - not implemented yet
    :param obs_stops_df: pandas data frame with the observed values of a stop.
     :return: scalar error value
    """
    set_impedence_values_run_assignment(visum, estimate_list)
    sim_stops = simulate_stop_ap_volumes(visum)
    stops_merged = obs_stops_df.merge(sim_stops, on="No")

    pax_trans_walkb_obs = stops_merged['PassTransWalkBoard(AP)_Obs']
    pax_trans_walkb_sim = stops_merged['PassTransWalkBoard(AP)_Sim']

    pax_trans_alightw_obs = stops_merged['PassTransAlightWalk(AP)_Obs']
    pax_trans_alightw_sim = stops_merged['PassTransAlightWalk(AP)_Sim']

    pass_trans_dir_obs = stops_merged['PassTransDir(AP)_Obs']
    pass_trans_dir_sim = stops_merged['PassTransDir(AP)_Sim']

    pass_trans_combined_obs = pax_trans_walkb_obs + pax_trans_alightw_obs + pass_trans_dir_obs
    pass_trans_combined_sim = pax_trans_walkb_sim + pax_trans_alightw_sim + pass_trans_dir_sim

    pass_trans_total_combined_rmsn = ec.calculate_rmsn(pass_trans_combined_obs, pass_trans_combined_sim)

    return pass_trans_total_combined_rmsn


def run_assignment_calculate_error_stops_pax_trans_combined_2(visum, estimate_list, obs_stops_df):
    """
    Calculates the error for PassTransWalkBoard(AP), PassTransAlightWalk(AP), PassTransDir(AP) in one list
    :param visum: Visum object
    :param estimate_list: A list, which contains the estimates in order [
    transfer_walk, origin_wait, transfer_wait, transfer penalty]
    :param obs_stops_df: pandas data frame with the observed values of a stop.
     :return: scalar error value
    """
    set_impedence_values_run_assignment_2(visum, estimate_list)
    sim_stops = simulate_stop_ap_volumes(visum)
    stops_merged = obs_stops_df.merge(sim_stops, on="No")

    pax_trans_walkb_obs = stops_merged['PassTransWalkBoard(AP)_Obs']
    pax_trans_walkb_sim = stops_merged['PassTransWalkBoard(AP)_Sim']

    pax_trans_alightw_obs = stops_merged['PassTransAlightWalk(AP)_Obs']
    pax_trans_alightw_sim = stops_merged['PassTransAlightWalk(AP)_Sim']

    pass_trans_dir_obs = stops_merged['PassTransDir(AP)_Obs']
    pass_trans_dir_sim = stops_merged['PassTransDir(AP)_Sim']

    pass_trans_combined_obs = pax_trans_walkb_obs + pax_trans_alightw_obs + pass_trans_dir_obs
    pass_trans_combined_sim = pax_trans_walkb_sim + pax_trans_alightw_sim + pass_trans_dir_sim

    pass_trans_total_combined_rmsn = ec.calculate_rmsn(pass_trans_combined_obs, pass_trans_combined_sim)

    return pass_trans_total_combined_rmsn


def run_assignment_calculate_error_stops_pax_trans_combined_all_para(visum, estimate_list, obs_stops_df):
    """
    Calculates the error for PassTransWalkBoard(AP), PassTransAlightWalk(AP), PassTransDir(AP) in one list
    :param visum: Visum object
    :param estimate_list: A list, which contains the estimates in order [
    transfer_walk, origin_wait, transfer_wait, transfer penalty]
    :param obs_stops_df: pandas data frame with the observed values of a stop.
     :return: scalar error value
    """
    set_impedence_values_run_assignment_all_para(visum, estimate_list)
    sim_stops = simulate_stop_ap_volumes(visum)
    stops_merged = obs_stops_df.merge(sim_stops, on="No")

    pax_trans_walkb_obs = stops_merged['PassTransWalkBoard(AP)_Obs']
    pax_trans_walkb_sim = stops_merged['PassTransWalkBoard(AP)_Sim']

    pax_trans_alightw_obs = stops_merged['PassTransAlightWalk(AP)_Obs']
    pax_trans_alightw_sim = stops_merged['PassTransAlightWalk(AP)_Sim']

    pass_trans_dir_obs = stops_merged['PassTransDir(AP)_Obs']
    pass_trans_dir_sim = stops_merged['PassTransDir(AP)_Sim']

    pass_trans_combined_obs = pax_trans_walkb_obs + pax_trans_alightw_obs + pass_trans_dir_obs  # pd. Series will add the values, not extend the list (this code calculated a wrong error)
    pass_trans_combined_sim = pax_trans_walkb_sim + pax_trans_alightw_sim + pass_trans_dir_sim

    pass_trans_total_combined_rmsn = ec.calculate_rmsn(pass_trans_combined_obs, pass_trans_combined_sim)

    return pass_trans_total_combined_rmsn


def runAssignmentCalculateErrorRMSN_all_error_terms(Visum, estimateList, obs_stops_df, obs_line_routes):
    set_impedence_values_run_assignment_2(Visum, estimateList)  # in_veh anchored
    # set_impedence_values_run_assignment_all_para(Visum, estimateList) #for all parameters
    sim_stops = simulate_stop_ap_volumes(Visum)
    sim_line_routes = simulate_line_route_ap_volumes(Visum)
    paxTripsWoCon = vlcs.getPuTStats(Visum)

    # Error terms from stops
    stops_merged = obs_stops_df.merge(sim_stops, on="No")

    pax_trans_total_obs = stops_merged["PassTransTotal(AP)_Obs"].tolist()
    pax_trans_total_sim = stops_merged["PassTransTotal(AP)_Sim"].tolist()

    pax_trans_walkb_obs = stops_merged["PassTransWalkBoard(AP)_Obs"].tolist()
    pax_trans_walkb_sim = stops_merged["PassTransWalkBoard(AP)_Sim"].tolist()

    pax_trans_alightw_obs = stops_merged["PassTransAlightWalk(AP)_Obs"].tolist()
    pax_trans_alightw_sim = stops_merged["PassTransAlightWalk(AP)_Sim"].tolist()

    pass_trans_dir_obs = stops_merged["PassTransDir(AP)_Obs"].tolist()
    pass_trans_dir_sim = stops_merged['PassTransDir(AP)_Sim'].tolist()

    pass_trans_combined_obs = pax_trans_walkb_obs + pax_trans_alightw_obs + pass_trans_dir_obs
    pass_trans_combined_sim = pax_trans_walkb_sim + pax_trans_alightw_sim + pass_trans_dir_sim

    pax_trans_walkb_transdir_combined_obs = pax_trans_walkb_obs + pass_trans_dir_obs
    pax_trans_walkb_trans_dir_combined_sim = pax_trans_walkb_sim + pass_trans_dir_sim

    pax_trans_total_rmsn = ec.calculate_rmsn(pax_trans_total_obs, pax_trans_total_sim)
    pax_trans_walkb_rmsn = ec.calculate_rmsn(pax_trans_walkb_obs, pax_trans_walkb_sim)
    pax_trans_alightw_rmsn = ec.calculate_rmsn(pax_trans_alightw_obs, pass_trans_dir_sim)
    pass_trans_dir_rmsn = ec.calculate_rmsn(pass_trans_dir_obs, pass_trans_dir_sim)

    # combined calculations
    pass_trans_total_combined_rmsn = ec.calculate_rmsn(pass_trans_combined_obs, pass_trans_combined_sim)
    mean_pax_trans_combined_rmsn = np.mean([pax_trans_walkb_rmsn, pax_trans_alightw_rmsn, pass_trans_dir_rmsn])
    pax_trans_walkb_trans_dir_combined_rmsn = ec.calculate_rmsn(pax_trans_walkb_transdir_combined_obs,
                                                                pax_trans_walkb_trans_dir_combined_sim)

    # sim_line_routes
    line_routes_merged = pd.merge(sim_line_routes, obs_line_routes, on=['LineName', 'Name'], how='left')

    pax_trips_unlinked_obs = line_routes_merged["PTripsUnlinked(AP)_Obs"].tolist()
    pax_trips_unlinked_sim = line_routes_merged["PTripsUnlinked(AP)_Sim"].tolist()

    pax_trips_unlinked_0_obs = line_routes_merged["PTripsUnlinked0(AP)_Obs"].tolist()
    pax_trips_unlinked_0_sim = line_routes_merged["PTripsUnlinked0(AP)_Sim"].tolist()

    pax_trips_unlinked_1_obs = line_routes_merged["PTripsUnlinked1(AP)_Obs"].tolist()
    pax_trips_unlinked_1_sim = line_routes_merged["PTripsUnlinked1(AP)_Sim"].tolist()

    pax_trips_unlinked_2_obs = line_routes_merged["PTripsUnlinked2(AP)_Obs"].tolist()
    pax_trips_unlinked_2_sim = line_routes_merged["PTripsUnlinked2(AP)_Sim"].tolist()

    pax_trips_unlinked_g_2_obs = line_routes_merged["PTripsUnlinked>2(AP)_Obs"].tolist()
    pax_trips_unlinked_g_2_sim = line_routes_merged["PTripsUnlinked>2(AP)_Sim"].tolist()

    pax_trips_unlinked_rmsn = ec.calculate_rmsn(pax_trips_unlinked_obs, pax_trips_unlinked_sim)
    pax_trips_unlinked_0_rmsn = ec.calculate_rmsn(pax_trips_unlinked_0_obs, pax_trips_unlinked_0_sim)
    pax_trips_unlinked_1_rmsn = ec.calculate_rmsn(pax_trips_unlinked_1_obs, pax_trips_unlinked_1_sim)
    pax_trips_unlinked_2_rmsn = ec.calculate_rmsn(pax_trips_unlinked_2_obs, pax_trips_unlinked_2_sim)
    pax_trips_unlinked_g_2_rmsn = ec.calculate_rmsn(pax_trips_unlinked_g_2_obs, pax_trips_unlinked_g_2_sim)

    dict = {}
    dict['pax_trans_total_rmsn'] = pax_trans_total_rmsn
    dict['pax_trans_walkb_rmsn'] = pax_trans_walkb_rmsn
    dict['pax_trans_alightw_rmsn'] = pax_trans_alightw_rmsn
    dict['pass_trans_dir_rmsn'] = pass_trans_dir_rmsn
    dict['pass_trans_total_combined_rmsn'] = pass_trans_total_combined_rmsn
    dict['mean_pax_trans_combined_rmsn'] = mean_pax_trans_combined_rmsn
    dict['pax_trans_walkb_trans_dir_combined_rmsn'] = pax_trans_walkb_trans_dir_combined_rmsn

    dict['pax_trips_unlinked_rmsn'] = pax_trips_unlinked_rmsn
    dict['pax_trips_unlinked_0_rmsn'] = pax_trips_unlinked_0_rmsn
    dict['pax_trips_unlinked_1_rmsn'] = pax_trips_unlinked_1_rmsn
    dict['pax_trips_unlinked_2_rmsn'] = pax_trips_unlinked_2_rmsn
    dict['pax_trips_unlinked_g_2_rmsn'] = pax_trips_unlinked_g_2_rmsn
    dict['paxTripsWoCon'] = paxTripsWoCon

    return dict


def runAssignmentCalculateError_rmsn_mape_all_error_terms(Visum, estimateList, obs_stops_df, obs_line_routes):
    set_impedence_values_run_assignment_2(Visum, estimateList)  # in_veh anchored
    # set_impedence_values_run_assignment_all_para(Visum, estimateList) #for all parameters
    sim_stops = simulate_stop_ap_volumes(Visum)
    sim_line_routes = simulate_line_route_ap_volumes(Visum)
    paxTripsWoCon = vlcs.getPuTStats(Visum)

    # Error terms from stops
    stops_merged = obs_stops_df.merge(sim_stops, on="No")

    pax_trans_total_obs = stops_merged["PassTransTotal(AP)_Obs"].tolist()
    pax_trans_total_sim = stops_merged["PassTransTotal(AP)_Sim"].tolist()

    pax_trans_walkb_obs = stops_merged["PassTransWalkBoard(AP)_Obs"].tolist()
    pax_trans_walkb_sim = stops_merged["PassTransWalkBoard(AP)_Sim"].tolist()

    pax_trans_alightw_obs = stops_merged["PassTransAlightWalk(AP)_Obs"].tolist()
    pax_trans_alightw_sim = stops_merged["PassTransAlightWalk(AP)_Sim"].tolist()

    pax_trans_dir_obs = stops_merged["PassTransDir(AP)_Obs"].tolist()
    pax_trans_dir_sim = stops_merged['PassTransDir(AP)_Sim'].tolist()

    pax_trans_combined_obs = pax_trans_walkb_obs + pax_trans_alightw_obs + pax_trans_dir_obs
    pax_trans_combined_sim = pax_trans_walkb_sim + pax_trans_alightw_sim + pax_trans_dir_sim

    pax_trans_walkb_transdir_combined_obs = pax_trans_walkb_obs + pax_trans_dir_obs
    pax_trans_walkb_trans_dir_combined_sim = pax_trans_walkb_sim + pax_trans_dir_sim

    pax_trans_total_rmsn = ec.calculate_rmsn(pax_trans_total_obs, pax_trans_total_sim)
    pax_trans_walkb_rmsn = ec.calculate_rmsn(pax_trans_walkb_obs, pax_trans_walkb_sim)
    pax_trans_alightw_rmsn = ec.calculate_rmsn(pax_trans_alightw_obs, pax_trans_alightw_sim)
    pax_trans_dir_rmsn = ec.calculate_rmsn(pax_trans_dir_obs, pax_trans_dir_sim)

    pax_trans_total_rmsn_0 = ec.calculate_rmsn_0(pax_trans_total_obs, pax_trans_total_sim)
    pax_trans_walkb_rmsn_0 = ec.calculate_rmsn_0(pax_trans_walkb_obs, pax_trans_walkb_sim)
    pax_trans_alightw_rmsn_0 = ec.calculate_rmsn_0(pax_trans_alightw_obs, pax_trans_alightw_sim)
    pax_trans_dir_rmsn_0 = ec.calculate_rmsn_0(pax_trans_dir_obs, pax_trans_dir_sim)

    pax_trans_total_mape = ec.calculate_mape(pax_trans_total_obs, pax_trans_total_sim)
    pax_trans_walkb_mape = ec.calculate_mape(pax_trans_walkb_obs, pax_trans_walkb_sim)
    pax_trans_alightw_mape = ec.calculate_mape(pax_trans_alightw_obs, pax_trans_alightw_sim)
    pax_trans_dir_mape = ec.calculate_mape(pax_trans_dir_obs, pax_trans_dir_sim)

    # combined calculations
    pax_trans_total_combined_rmsn = ec.calculate_rmsn(pax_trans_combined_obs, pax_trans_combined_sim)
    pax_trans_total_combined_rmsn_0 = ec.calculate_rmsn_0(pax_trans_combined_obs, pax_trans_combined_sim)
    pax_trans_total_combined_mape = ec.calculate_mape(pax_trans_combined_obs, pax_trans_combined_sim)

    mean_pax_trans_combined_rmsn = np.mean([pax_trans_walkb_rmsn, pax_trans_alightw_rmsn, pax_trans_dir_rmsn])
    pax_trans_walkb_trans_dir_combined_rmsn = ec.calculate_rmsn(pax_trans_walkb_transdir_combined_obs,
                                                                pax_trans_walkb_trans_dir_combined_sim)

    # sim_line_routes
    line_routes_merged = pd.merge(sim_line_routes, obs_line_routes, on=['LineName', 'Name'], how='left')

    pax_trips_unlinked_obs = line_routes_merged["PTripsUnlinked(AP)_Obs"].tolist()
    pax_trips_unlinked_sim = line_routes_merged["PTripsUnlinked(AP)_Sim"].tolist()

    pax_trips_unlinked_0_obs = line_routes_merged["PTripsUnlinked0(AP)_Obs"].tolist()
    pax_trips_unlinked_0_sim = line_routes_merged["PTripsUnlinked0(AP)_Sim"].tolist()

    pax_trips_unlinked_1_obs = line_routes_merged["PTripsUnlinked1(AP)_Obs"].tolist()
    pax_trips_unlinked_1_sim = line_routes_merged["PTripsUnlinked1(AP)_Sim"].tolist()

    pax_trips_unlinked_2_obs = line_routes_merged["PTripsUnlinked2(AP)_Obs"].tolist()
    pax_trips_unlinked_2_sim = line_routes_merged["PTripsUnlinked2(AP)_Sim"].tolist()

    pax_trips_unlinked_g_2_obs = line_routes_merged["PTripsUnlinked>2(AP)_Obs"].tolist()
    pax_trips_unlinked_g_2_sim = line_routes_merged["PTripsUnlinked>2(AP)_Sim"].tolist()

    pax_trips_unlinked_rmsn = ec.calculate_rmsn(pax_trips_unlinked_obs, pax_trips_unlinked_sim)
    pax_trips_unlinked_0_rmsn = ec.calculate_rmsn(pax_trips_unlinked_0_obs, pax_trips_unlinked_0_sim)
    pax_trips_unlinked_1_rmsn = ec.calculate_rmsn(pax_trips_unlinked_1_obs, pax_trips_unlinked_1_sim)
    pax_trips_unlinked_2_rmsn = ec.calculate_rmsn(pax_trips_unlinked_2_obs, pax_trips_unlinked_2_sim)
    pax_trips_unlinked_g_2_rmsn = ec.calculate_rmsn(pax_trips_unlinked_g_2_obs, pax_trips_unlinked_g_2_sim)

    pax_trips_unlinked_rmsn_0 = ec.calculate_rmsn_0(pax_trips_unlinked_obs, pax_trips_unlinked_sim)
    pax_trips_unlinked_0_rmsn_0 = ec.calculate_rmsn_0(pax_trips_unlinked_0_obs, pax_trips_unlinked_0_sim)
    pax_trips_unlinked_1_rmsn_0 = ec.calculate_rmsn_0(pax_trips_unlinked_1_obs, pax_trips_unlinked_1_sim)
    pax_trips_unlinked_2_rmsn_0 = ec.calculate_rmsn_0(pax_trips_unlinked_2_obs, pax_trips_unlinked_2_sim)
    pax_trips_unlinked_g_2_rmsn_0 = ec.calculate_rmsn_0(pax_trips_unlinked_g_2_obs, pax_trips_unlinked_g_2_sim)

    pax_trips_unlinked_mape = ec.calculate_mape(pax_trips_unlinked_obs, pax_trips_unlinked_sim)
    pax_trips_unlinked_0_mape = ec.calculate_mape(pax_trips_unlinked_0_obs, pax_trips_unlinked_0_sim)
    pax_trips_unlinked_1_mape = ec.calculate_mape(pax_trips_unlinked_1_obs, pax_trips_unlinked_1_sim)
    pax_trips_unlinked_2_mape = ec.calculate_mape(pax_trips_unlinked_2_obs, pax_trips_unlinked_2_sim)
    pax_trips_unlinked_g_2_mape = ec.calculate_mape(pax_trips_unlinked_g_2_obs, pax_trips_unlinked_g_2_sim)

    dict = {}
    # RMSN
    dict['pax_trans_total_rmsn'] = pax_trans_total_rmsn
    dict['pax_trans_walkb_rmsn'] = pax_trans_walkb_rmsn
    dict['pax_trans_alightw_rmsn'] = pax_trans_alightw_rmsn
    dict['pax_trans_dir_rmsn'] = pax_trans_dir_rmsn
    dict['pax_trans_total_combined_rmsn'] = pax_trans_total_combined_rmsn

    # RMSN omit zero
    dict['pax_trans_total_rmsn_0'] = pax_trans_total_rmsn_0
    dict['pax_trans_walkb_rmsn_0'] = pax_trans_walkb_rmsn_0
    dict['pax_trans_alightw_rmsn_0'] = pax_trans_alightw_rmsn_0
    dict['pax_trans_dir_rmsn_0'] = pax_trans_dir_rmsn_0
    dict['pax_trans_total_combined_rmsn_0'] = pax_trans_total_combined_rmsn_0


    # MAPE
    dict['pax_trans_total_mape'] = pax_trans_total_mape
    dict['pax_trans_walkb_mape'] = pax_trans_walkb_mape
    dict['pax_trans_alightw_mape'] = pax_trans_alightw_mape
    dict['pax_trans_dir_mape'] = pax_trans_dir_mape
    dict['pax_trans_total_combined_mape'] = pax_trans_total_combined_mape

    dict['mean_pax_trans_combined_rmsn'] = mean_pax_trans_combined_rmsn
    dict['pax_trans_walkb_trans_dir_combined_rmsn'] = pax_trans_walkb_trans_dir_combined_rmsn

    # RMSN
    dict['pax_trips_unlinked_rmsn'] = pax_trips_unlinked_rmsn
    dict['pax_trips_unlinked_0_rmsn'] = pax_trips_unlinked_0_rmsn
    dict['pax_trips_unlinked_1_rmsn'] = pax_trips_unlinked_1_rmsn
    dict['pax_trips_unlinked_2_rmsn'] = pax_trips_unlinked_2_rmsn
    dict['pax_trips_unlinked_g_2_rmsn'] = pax_trips_unlinked_g_2_rmsn

    #RMSN omit zero
    dict['pax_trips_unlinked_rmsn_0'] = pax_trips_unlinked_rmsn_0
    dict['pax_trips_unlinked_0_rmsn_0'] = pax_trips_unlinked_0_rmsn_0
    dict['pax_trips_unlinked_1_rmsn_0'] = pax_trips_unlinked_1_rmsn_0
    dict['pax_trips_unlinked_2_rmsn_0'] = pax_trips_unlinked_2_rmsn_0
    dict['pax_trips_unlinked_g_2_rmsn_0'] = pax_trips_unlinked_g_2_rmsn_0

    # MAPE
    dict['pax_trips_unlinked_mape'] = pax_trips_unlinked_mape
    dict['pax_trips_unlinked_0_mape'] = pax_trips_unlinked_0_mape
    dict['pax_trips_unlinked_1_mape'] = pax_trips_unlinked_1_mape
    dict['pax_trips_unlinked_2_mape'] = pax_trips_unlinked_2_mape
    dict['pax_trips_unlinked_g_2_mape'] = pax_trips_unlinked_g_2_mape

    dict['paxTripsWoCon'] = paxTripsWoCon

    return dict


def simulate_line_route_ap_volumes(Visum):
    simulatedDataFrame = vlcs.createLineRouteListDataFrame(Visum)
    changeColNamesDic = {"PTripsUnlinked(AP)": "PTripsUnlinked(AP)_Sim",
                         "PTripsUnlinked0(AP)": "PTripsUnlinked0(AP)_Sim",
                         "PTripsUnlinked1(AP)": "PTripsUnlinked1(AP)_Sim",
                         "PTripsUnlinked2(AP)": "PTripsUnlinked2(AP)_Sim",
                         "PTripsUnlinked>2(AP)": "PTripsUnlinked>2(AP)_Sim"
                         }
    simulatedDataFrame = simulatedDataFrame.rename(columns=changeColNamesDic)

    simulatedDataFrame["LineName"] = simulatedDataFrame["LineName"].astype(str)
    simulatedDataFrame["Name"] = simulatedDataFrame["Name"].astype(str)

    return simulatedDataFrame


def simulate_stop_ap_volumes(Visum):
    simulatedDataFrame = vlcs.createStopsListDataFrame(Visum)
    changeColNamesDic = {"PassTransTotal(AP)": "PassTransTotal(AP)_Sim", "PassTransDir(AP)": "PassTransDir(AP)_Sim",
                         "PassTransWalkBoard(AP)": "PassTransWalkBoard(AP)_Sim",
                         "PassTransAlightWalk(AP)": "PassTransAlightWalk(AP)_Sim"
                         }

    simulatedDataFrame = simulatedDataFrame.rename(columns=changeColNamesDic)

    return simulatedDataFrame


def set_impedence_values_run_assignment(Visum, estimate_list):
    # for singapore network
    inVehTime_c = estimate_list[0]
    transferWalkTime_c = estimate_list[1]
    originWaitTime_c = estimate_list[2]
    transferWaitTime_c = estimate_list[3]

    # setting attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(
        2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters

    impedenceParaObject.SetAttValue("INVEHTIMEVAL", str(inVehTime_c))
    impedenceParaObject.SetAttValue("WALKTIMEVAL", str(transferWalkTime_c))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", str(originWaitTime_c))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", str(transferWaitTime_c))

    Visum.Procedures.Execute()


def set_impedence_values_run_assignment_2(Visum, estimate_list):
    """in vehicle time is set to 1
        transfer penalty is calibrated
    """
    # for singapore network

    transferWalkTime_c = estimate_list[0]
    originWaitTime_c = estimate_list[1]
    transferWaitTime_c = estimate_list[2]
    transferPenalty = estimate_list[3] * 60.0

    # setting attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(
        2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters

    impedenceParaObject.SetAttValue("WALKTIMEVAL", float(transferWalkTime_c))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", float(originWaitTime_c))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", float(transferWaitTime_c))
    impedenceParaObject.SetAttValue("NUMTRANSFERSVAL", float(transferPenalty))

    Visum.Procedures.Execute()


def set_impedence_values_run_assignment_all_para(Visum, estimate_list):
    """in vehicle time is set to 1
        transfer penalty is calibrated
    """
    # for singapore network
    inVehTime_c = estimate_list[0]
    transferWalkTime_c = estimate_list[1]
    originWaitTime_c = estimate_list[2]
    transferWaitTime_c = estimate_list[3]
    transferPenalty = estimate_list[4] * 60.0

    # setting attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(
        2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters

    impedenceParaObject.SetAttValue("INVEHTIMEVAL", str(inVehTime_c))
    impedenceParaObject.SetAttValue("WALKTIMEVAL", float(transferWalkTime_c))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", float(originWaitTime_c))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", float(transferWaitTime_c))
    impedenceParaObject.SetAttValue("NUMTRANSFERSVAL", float(transferPenalty))

    Visum.Procedures.Execute()


# Saving the error values calculated to a dictionary and then to a dataframe
def parse_error_from_dict_to_df(simulated_error_dict, current_estimate, objective_function):
    df_columns = ['objective_function',

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

    temp_dict = {}
    return_df = pd.DataFrame(columns=df_columns)
    # temp_dict['in_vehicle'] = current_estimate[0]
    # temp_dict['transfer_walk'] = current_estimate[1]
    # temp_dict['origin_wait'] = current_estimate[2]
    # temp_dict['transfer_wait'] = current_estimate[3]
    # temp_dict['transfer_penalty'] = current_estimate[4]

    temp_dict['objective_function'] = objective_function

    temp_dict['pax_trans_total_rmsn'] = simulated_error_dict['pax_trans_total_rmsn']
    temp_dict['pax_trans_walkb_rmsn'] = simulated_error_dict['pax_trans_walkb_rmsn']
    temp_dict['pax_trans_alightw_rmsn'] = simulated_error_dict['pax_trans_alightw_rmsn']
    temp_dict['pax_trans_dir_rmsn'] = simulated_error_dict['pax_trans_dir_rmsn']
    temp_dict['pax_trans_total_combined_rmsn'] = simulated_error_dict['pax_trans_total_combined_rmsn']

    temp_dict['pax_trans_total_rmsn_0'] = simulated_error_dict['pax_trans_total_rmsn_0']
    temp_dict['pax_trans_walkb_rmsn_0'] = simulated_error_dict['pax_trans_walkb_rmsn_0']
    temp_dict['pax_trans_alightw_rmsn_0'] = simulated_error_dict['pax_trans_alightw_rmsn_0']
    temp_dict['pax_trans_dir_rmsn_0'] = simulated_error_dict['pax_trans_dir_rmsn_0']
    temp_dict['pax_trans_total_combined_rmsn_0'] = simulated_error_dict['pax_trans_total_combined_rmsn_0']

    temp_dict['pax_trans_total_mape'] = simulated_error_dict['pax_trans_total_mape']
    temp_dict['pax_trans_walkb_mape'] = simulated_error_dict['pax_trans_walkb_mape']
    temp_dict['pax_trans_alightw_mape'] = simulated_error_dict['pax_trans_alightw_mape']
    temp_dict['pax_trans_dir_mape'] = simulated_error_dict['pax_trans_dir_mape']
    temp_dict['pax_trans_total_combined_mape'] = simulated_error_dict['pax_trans_total_combined_mape']

    temp_dict['mean_pax_trans_combined_rmsn'] = simulated_error_dict['mean_pax_trans_combined_rmsn']
    temp_dict['pax_trans_walkb_trans_dir_combined_rmsn'] = simulated_error_dict[
        'pax_trans_walkb_trans_dir_combined_rmsn']

    temp_dict['pax_trips_unlinked_rmsn'] = simulated_error_dict['pax_trips_unlinked_rmsn']
    temp_dict['pax_trips_unlinked_0_rmsn'] = simulated_error_dict['pax_trips_unlinked_0_rmsn']
    temp_dict['pax_trips_unlinked_1_rmsn'] = simulated_error_dict['pax_trips_unlinked_1_rmsn']
    temp_dict['pax_trips_unlinked_2_rmsn'] = simulated_error_dict['pax_trips_unlinked_2_rmsn']
    temp_dict['pax_trips_unlinked_g_2_rmsn'] = simulated_error_dict['pax_trips_unlinked_g_2_rmsn']

    temp_dict['pax_trips_unlinked_rmsn_0'] = simulated_error_dict['pax_trips_unlinked_rmsn_0']
    temp_dict['pax_trips_unlinked_0_rmsn_0'] = simulated_error_dict['pax_trips_unlinked_0_rmsn_0']
    temp_dict['pax_trips_unlinked_1_rmsn_0'] = simulated_error_dict['pax_trips_unlinked_1_rmsn_0']
    temp_dict['pax_trips_unlinked_2_rmsn_0'] = simulated_error_dict['pax_trips_unlinked_2_rmsn_0']
    temp_dict['pax_trips_unlinked_g_2_rmsn_0'] = simulated_error_dict['pax_trips_unlinked_g_2_rmsn_0']

    temp_dict['pax_trips_unlinked_mape'] = simulated_error_dict['pax_trips_unlinked_mape']
    temp_dict['pax_trips_unlinked_0_mape'] = simulated_error_dict['pax_trips_unlinked_0_mape']
    temp_dict['pax_trips_unlinked_1_mape'] = simulated_error_dict['pax_trips_unlinked_1_mape']
    temp_dict['pax_trips_unlinked_2_mape'] = simulated_error_dict['pax_trips_unlinked_2_mape']
    temp_dict['pax_trips_unlinked_g_2_mape'] = simulated_error_dict['pax_trips_unlinked_g_2_mape']

    temp_dict['transfer_walk'] = current_estimate[0]
    temp_dict['origin_wait'] = current_estimate[1]
    temp_dict['transfer_wait'] = current_estimate[2]
    temp_dict['transfer_penalty'] = current_estimate[3]
    temp_dict['paxTripsWoCon'] = simulated_error_dict['paxTripsWoCon']


    temp_df = pd.DataFrame(temp_dict, index=[0])
    return_df = return_df.append(temp_df)

    return return_df


def select_better_objective_function(inc_obj_list, dec_obj_list, obj_function_list):
    """return a name of the objective function with the highest relative change as a string"""

    obj_func_1_inc = inc_obj_list[0]
    obj_func_1_dec = dec_obj_list[0]

    obj_func_2_inc = inc_obj_list[1]
    obj_func_2_dec = dec_obj_list[1]

    #obj_func_3_inc = inc_obj_list[2]
    #obj_func_3_dec = dec_obj_list[2]

    rel_change_obj_1 = (obj_func_1_inc - obj_func_1_dec) / np.mean([obj_func_1_inc, obj_func_1_dec])
    rel_change_obj_2 = (obj_func_2_inc - obj_func_2_dec) / np.mean([obj_func_2_inc, obj_func_2_dec])
    #rel_change_obj_3 = (obj_func_3_inc - obj_func_3_dec) / np.mean([obj_func_3_inc, obj_func_3_dec])

    rel_change_list = [rel_change_obj_1, rel_change_obj_2]
    max_index = rel_change_list.index(max(rel_change_list))

    return obj_function_list[max_index]
