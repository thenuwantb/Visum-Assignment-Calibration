'''
Created on 14 Jan 2020

@author: thenuwan.jayasinghe
'''
import custom_visum_functions.visum_list_calculations.list_calculations as vlc
import custom_visum_functions.satistical_calculations.error_calculations as ec
import pandas as pd



def runAssignmentCalculateErrorRMSN(Visum, estimateList, obsStopPoints, obsTransferWalk):
    
    
    #Run Assignment and create dataframes for simulated values
    setImpedenceValuesAndRunAssignment(Visum, estimateList)
    simStopPoints = simulateStopPointValues(Visum)
    simTransferWalk = simulateTransferWalkTimeValues(Visum)
    #simConnectorVolumes = simulateConnectorVolumes(Visum)
    
    #merge the simulated values and observed values
    stopPoints_merged = obsStopPoints.merge(simStopPoints, on = ["No", "StopAreaNo", "NodeNo"])
    transferWalk_merged = obsTransferWalk.merge(simTransferWalk, on = ["StopNo", "FromStopAreaNo", "ToStopAreaNo"])
    #connectorVolumes_merged = obsConnectorVolumes.merge(simConnectorVolumes, on = ["ZoneNo", "NodeNo", "Direction"])
    
    #Take observed and simulated values to lists
    passTransWalkBoard_obs = stopPoints_merged['PassTransWalkBoard(AP)_Obs'].tolist()
    passTransWalkBoard_sim = stopPoints_merged['PassTransWalkBoard(AP)_Sim'].tolist()
    
    passTransAlightWalk_obs = stopPoints_merged['PassTransAlightWalk(AP)_Obs'].tolist()
    passTransAlightWalk_sim = stopPoints_merged['PassTransAlightWalk(AP)_Sim'].tolist()
    
    transferWaitTime_obs = stopPoints_merged['TransferWaitTime(AP)_Obs'].tolist()
    transferWaitTime_sim = stopPoints_merged['TransferWaitTime(AP)_Sim'].tolist()
    
    passTransWalk_obs = transferWalk_merged['PassTransTotal(AP)_Obs'].tolist()
    passTransWalk_sim = transferWalk_merged['PassTransTotal(AP)_Sim'].tolist()
    
    #connectorVolume_obs = connectorVolumes_merged['VolPersPuT(AP)_Obs'].tolist()
    #connectorVolume_sim = connectorVolumes_merged['VolPersPuT(AP)_Sim'].tolist()
    
    #calculate RMSN
    passTransWalkBoard_rmsn = ec.calculateRMSN(passTransWalkBoard_obs, passTransWalkBoard_sim)
    passTransAlightWalk_rmsn = ec.calculateRMSN(passTransAlightWalk_obs, passTransAlightWalk_sim)
    transferWaitTime_rmsn = ec.calculateRMSN(transferWaitTime_obs, transferWaitTime_sim)
    passTransWalk_rmsn = ec.calculateRMSN(passTransWalk_obs, passTransWalk_sim)
    #connectorVolume_rmsn = ec.calculateRMSN(connectorVolume_obs, connectorVolume_sim)
    
    total_rmsn = passTransWalkBoard_rmsn + passTransAlightWalk_rmsn # + transferWaitTime_rmsn + passTransWalk_rmsn
    
    return total_rmsn
    
    
def simulateStopPointValues(Visum):
    simulatedDataFrame = vlc.createStopPointsDataFrame(Visum)
    changeColNamesDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Sim", "PassTransDir(AP)" : "PassTransDir(AP)_Sim", "PassTransWalkBoard(AP)" : "PassTransWalkBoard(AP)_Sim", 
                      "PassTransAlightWalk(AP)" : "PassTransAlightWalk(AP)_Sim", "TransferWaitTime(AP)" : "TransferWaitTime(AP)_Sim"}
    
    simulatedDataFrame = simulatedDataFrame.rename(columns = changeColNamesDic)
    
    return simulatedDataFrame
    

def simulateTransferWalkTimeValues(Visum):
    simulatedDataFrame = vlc.createStopTransferWalkTimeDataFrame(Visum)
    changeColNamesDic = {"PassTransTotal(AP)" : "PassTransTotal(AP)_Sim"}
    
    simulatedDataFrame = simulatedDataFrame.rename(columns = changeColNamesDic)
    
    return simulatedDataFrame

def simulateConnectorVolumes(Visum):
    simulatedDataFrame = vlc.createConnectorListDataFrame(Visum)
    changeColNamesDic = {"VolPersPuT(AP)" : "VolPersPuT(AP)_Sim"}
    simulatedDataFrame = simulatedDataFrame.rename(columns = changeColNamesDic)
    
    return simulatedDataFrame


def setImpedenceValuesAndRunAssignment(Visum, estimateList): #Amendment to executeVisumProceduresWithEstimates_stopPointList - 08012020
    inVehTime_c = estimateList[0]
    accessTime_c = estimateList[1]
    egressTime_c = estimateList[2]
    transferWalkTime_c = estimateList[3]
    originWaitTime_c = estimateList[4]
    transferWaitTime_c = estimateList[5]
    
    # setting attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters
    
    impedenceParaObject.SetAttValue("INVEHTIMEVAL", str(inVehTime_c))
    impedenceParaObject.SetAttValue("ACCESSTIMEVAL", str(accessTime_c))
    impedenceParaObject.SetAttValue("EGRESSTIMEVAL", str(egressTime_c))
    impedenceParaObject.SetAttValue("WALKTIMEVAL", str(transferWalkTime_c))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", str(originWaitTime_c))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", str(transferWaitTime_c))
    
    Visum.Procedures.Execute()
    
