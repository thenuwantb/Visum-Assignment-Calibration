'''
Created on 2 Dec 2019

@author: thenuwan.jayasinghe
'''
import os.path

import pandas as pd
import xml.etree.ElementTree as ET

#import customVisumFunctions.statisticalCalculations as sc

path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\1_VISUM_Simple"
verFile = "2_Simple_Network.ver"
versionPath = os.path.join(path, verFile)


def totalPaxKmTravelAP(Visum):
    lineRouteList = Visum.Lists.CreateLineList
    lineRouteList.AddColumn("PassKmTrav(AP)")
    lineRouteListArray = lineRouteList.SaveToArray()
    lineRouteListDF = pd.DataFrame(list(lineRouteListArray))
    
    return sum(lineRouteListDF[0])


def totalPaxKmTravelAP_PJTPara(Visum, list_of_PJT_Para):
    '''returns the value of totalPaxKmTravelAP() with estimated PJT values'''
    # initialGuess = [inVehTimeC, walkTimeC, originWaitTimeC, transferWaitTimeC, transferPenaltyC]
    
    # check for a better way (like tuple breakdown)
    inVehTimeC = list_of_PJT_Para[0]
    walkTimeC = list_of_PJT_Para[1]
    originWaitTimeC = list_of_PJT_Para[2]
    transferWaitTimeC = list_of_PJT_Para[3]
    # transferPenaltyC = list_of_PJT_Para[4]
    
    # setting the attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters
    
    impedenceParaObject.SetAttValue("INVEHTIMEVAL", str(inVehTimeC))
    impedenceParaObject.SetAttValue("WALKTIMEVAL", str(walkTimeC))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", str(originWaitTimeC))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", str(transferWaitTimeC))
    # impedenceParaObject.SetAttValue("NUMTRANSFERSVAL", str(transferPenaltyC))
        
    Visum.Procedures.Execute()
    
    total = totalPaxKmTravelAP(Visum)
    return total


def totalPaxKmTravelAP_PJTPara_xml(Visum, list_of_PJT_Para, proc_para_savepath):
    _inVehTime = list_of_PJT_Para[0]
    _walkTime = list_of_PJT_Para[1]
    _originWaitTime = list_of_PJT_Para[2]
    _transferWaitTime = list_of_PJT_Para[3]
    
    Visum.Procedures.Save(proc_para_savepath)
    
    tree = ET.parse(proc_para_savepath)
    root = tree.getroot()
    headwayImpedencepara = root[1][1][0][0][3]
    
    # changing the coefficients
    headwayImpedencepara.set("INVEHTIMEVAL", str(_inVehTime))
    headwayImpedencepara.set("WALKTIMEVAL", str(_walkTime))
    headwayImpedencepara.set("ORIGINWAITTIMEVAL", str(_originWaitTime))
    headwayImpedencepara.set("TRANSFERWAITTIMEVAL", str(_transferWaitTime))
    
    # write back to the same file
    tree.write(proc_para_savepath)
    
    # Remove old ones
    Visum.Procedures.Operations.RemoveOperation(1)
    Visum.Procedures.Operations.RemoveOperation(1)
    
    # Add the procedures again
    Visum.Procedures.Open(proc_para_savepath)
    Visum.Procedures.Execute()
    
    total = totalPaxKmTravelAP(Visum)
    return total




def createLinkListDataFrame(Visum):
    visumLinkList = Visum.Lists.CreateLinkList
    visumLinkList.AddColumn("No")
    visumLinkList.AddColumn("FromNodeNo")
    visumLinkList.AddColumn("ToNodeNo")
    visumLinkList.AddColumn("VolPers_DSeg_TSys(X-B,AP)")
  
    linkListArray = visumLinkList.SaveToArray()
    linkListDataFrame = pd.DataFrame(list(linkListArray),
                                     columns=["No", "FromNodeNo", "ToNodeNo", "VolPers_DSeg_TSys(X-B,AP)"])
    
    linkListDataFrame['No'] = (linkListDataFrame['No'].astype(int)).astype(str)
    linkListDataFrame['FromNodeNo'] = (linkListDataFrame['FromNodeNo'].astype(int)).astype(str)
    linkListDataFrame['ToNodeNo'] = (linkListDataFrame['ToNodeNo'].astype(int)).astype(str)
    linkListDataFrame['VolPers_DSeg_TSys(X-B,AP)'] = linkListDataFrame['VolPers_DSeg_TSys(X-B,AP)'].astype(float)
    
    linkListDataFrame['Key'] = linkListDataFrame['No'] + linkListDataFrame['FromNodeNo'] + linkListDataFrame['ToNodeNo']
    linkListDataFrame = linkListDataFrame[['No', 'FromNodeNo', 'ToNodeNo', 'Key', 'VolPers_DSeg_TSys(X-B,AP)']]  # to order the dataframe
   
    return linkListDataFrame


def executeVisumProceduresWithEstimates_linkList(Visum, estimate_list):
     
    # check for a better way (like tuple breakdown)
    inVehTimeC = estimate_list[0]
    walkTimeC = estimate_list[1]
    originWaitTimeC = estimate_list[2]
    transferWaitTimeC = estimate_list[3]
    # transferPenaltyC = list_of_PJT_Para[4]
    
    # setting the attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters
    
    impedenceParaObject.SetAttValue("INVEHTIMEVAL", str(inVehTimeC))
    impedenceParaObject.SetAttValue("WALKTIMEVAL", str(walkTimeC))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", str(originWaitTimeC))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", str(transferWaitTimeC))
    # impedenceParaObject.SetAttValue("NUMTRANSFERSVAL", str(transferPenaltyC))
        
    Visum.Procedures.Execute()
    
    linkListDf_Simulated = createLinkListDataFrame(Visum)
    return linkListDf_Simulated

    
def calcErrorLinklistSimulatedAndObserved(Visum, observedLinkListDf, estimateList):

    simulatedLinkListDf = executeVisumProceduresWithEstimates_linkList(Visum, estimateList)
    
    simulatedLinkListDf = simulatedLinkListDf.rename(columns={'VolPers_DSeg_TSys(X-B,AP)' : 'Simulated_Values'})

    comparisonTableDf = observedLinkListDf.merge(simulatedLinkListDf, on='Key')
    # print comparisonTableDf[['Key', 'Observed_Values', 'Simulated_Values']]

    # print comparison_table.columns.values

    # print comparison_table[['Observed_Values', 'Simulated_Values']]

    observedValuesList = comparisonTableDf['Observed_Values'].tolist()
    simulatedValuesList = comparisonTableDf['Simulated_Values'].tolist()
    
    error_1 = sc.calculateRMSN(observedValuesList, simulatedValuesList)
    
    return error_1


def createStopPointListDataFrame(Visum):
    visumStopPointList = Visum.Lists.CreateStopPointBaseList
    visumStopPointList.AddColumn("No")
    visumStopPointList.AddColumn("StopAreaNo")
    visumStopPointList.AddColumn("NodeNo")
    visumStopPointList.AddColumn("PassTransTotal(AP)")
    
    stopPointListArray = visumStopPointList.SaveToArray()
    stopPointListDataFrame = pd.DataFrame(list(stopPointListArray), columns=["No", "StopAreaNo", "NodeNo", "PassTransTotal(AP)"])
    
    stopPointListDataFrame['No'] = (stopPointListDataFrame['No'].astype(int)).astype(str)
    stopPointListDataFrame['StopAreaNo'] = (stopPointListDataFrame['StopAreaNo'].astype(int)).astype(str)
    stopPointListDataFrame['NodeNo'] = (stopPointListDataFrame['NodeNo'].astype(int)).astype(str)
    stopPointListDataFrame['PassTransTotal(AP)'] = stopPointListDataFrame['PassTransTotal(AP)'].astype(float)
    
    stopPointListDataFrame['Key'] = stopPointListDataFrame['No'] + stopPointListDataFrame['StopAreaNo'] + stopPointListDataFrame['NodeNo']
    stopPointListDataFrame = stopPointListDataFrame[['No', 'StopAreaNo', 'NodeNo', 'Key', 'PassTransTotal(AP)']]
    
    return stopPointListDataFrame


def executeVisumProceduresWithEstimates_stopPointList(Visum, estimate_list):
     
    # check for a better way (like tuple breakdown)
    inVehTimeC = estimate_list[0]
    walkTimeC = estimate_list[1]
    originWaitTimeC = estimate_list[2]
    transferWaitTimeC = estimate_list[3]
    # transferPenaltyC = list_of_PJT_Para[4]
    
    # setting the attribute values of headway based assignment
    impedenceParaObject = Visum.Procedures.Operations.ItemByKey(2).PuTAssignmentParameters.HeadwayBasedParameters.ImpedanceParameters
    
    impedenceParaObject.SetAttValue("INVEHTIMEVAL", str(inVehTimeC))
    impedenceParaObject.SetAttValue("WALKTIMEVAL", str(walkTimeC))
    impedenceParaObject.SetAttValue("ORIGINWAITTIMEVAL", str(originWaitTimeC))
    impedenceParaObject.SetAttValue("TRANSFERWAITTIMEVAL", str(transferWaitTimeC))
    # impedenceParaObject.SetAttValue("NUMTRANSFERSVAL", str(transferPenaltyC))
        
    Visum.Procedures.Execute()
    
    stopPointListtDf_Simulated = createStopPointListDataFrame(Visum)
    return stopPointListtDf_Simulated


def calcErrorStopPointSimulatedAndObserved(Visum, observedStopPointList, estimateList):

    simulatedStopPointListDf = executeVisumProceduresWithEstimates_stopPointList(Visum, estimateList)
    
    simulatedStopPointListDf = simulatedStopPointListDf.rename(columns={'PassTransTotal(AP)' : 'Simulated_Values'})

    comparisonTableDf = observedStopPointList.merge(simulatedStopPointListDf, on='Key')

    observedValuesList = comparisonTableDf['Observed_Values'].tolist()
    simulatedValuesList = comparisonTableDf['Simulated_Values'].tolist()
    
    error_2 = sc.calculateRMSN(observedValuesList, simulatedValuesList)
    
    return error_2
    
