'''
Created on 14 Jan 2020

@author: thenuwan.jayasinghe
'''
import custom_visum_functions.visum_list_calculations.list_calculations_singapore as vlcs
import custom_visum_functions.satistical_calculations.error_calculations as ec
import pandas as pd


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

    pass_trans_total_rmsn = ec.calculateRMSN(pax_trans_total_obs, pax_trans_total_sim)

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

    pass_trans_total_combined_rmsn = ec.calculateRMSN(pass_trans_combined_obs, pass_trans_combined_sim)

    return pass_trans_total_combined_rmsn


def simulateLineRouteVolumes(Visum):
    simulatedDataFrame = vlcs.createLineRouteListDataFrame(Visum)
    changeColNamesDic = {"PTripsUnlinked0(AP)": "PTripsUnlinked0(AP)_Sim",
                         "PTripsUnlinked1(AP)": "PTripsUnlinked1(AP)_Sim"}
    simulatedDataFrame = simulatedDataFrame.rename(columns=changeColNamesDic)

    simulatedDataFrame["LineName"] = simulatedDataFrame["LineName"].astype(str)
    simulatedDataFrame["Name"] = simulatedDataFrame["Name"].astype(str)
    # simulatedDataFrame["Direction"] = simulatedDataFrame["Direction"].astype(str)

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
