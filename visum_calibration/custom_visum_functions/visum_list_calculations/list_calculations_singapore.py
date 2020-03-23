'''
Created on 2 Dec 2019

@author: thenuwan.jayasinghe
'''
import os.path

import pandas as pd
import xml.etree.ElementTree as ET
import custom_visum_functions.satistical_calculations.error_calculations as ec


def createStopPointListDataFrame(Visum):
    visumStopPointList = Visum.Lists.CreateStopPointBaseList
    visumStopPointList.AddColumn("No")
    visumStopPointList.AddColumn("StopAreaNo")
    visumStopPointList.AddColumn("NodeNo")
    visumStopPointList.AddColumn("PassTransTotal(AP)")

    stopPointListArray = visumStopPointList.SaveToArray()
    stopPointListDataFrame = pd.DataFrame(list(stopPointListArray),
                                          columns=["No", "StopAreaNo", "NodeNo", "PassTransTotal(AP)"])

    stopPointListDataFrame['No'] = (stopPointListDataFrame['No'].astype(int)).astype(str)
    stopPointListDataFrame['StopAreaNo'] = (stopPointListDataFrame['StopAreaNo'].astype(int)).astype(str)
    stopPointListDataFrame['NodeNo'] = (stopPointListDataFrame['NodeNo'].astype(int)).astype(str)
    stopPointListDataFrame['PassTransTotal(AP)'] = stopPointListDataFrame['PassTransTotal(AP)'].astype(float)

    stopPointListDataFrame['Key'] = stopPointListDataFrame['No'] + stopPointListDataFrame['StopAreaNo'] + \
                                    stopPointListDataFrame['NodeNo']
    stopPointListDataFrame = stopPointListDataFrame[['No', 'StopAreaNo', 'NodeNo', 'Key', 'PassTransTotal(AP)']]

    return stopPointListDataFrame


def createStopPointsDataFrame(Visum):  # Amendment to createStopPointListDataFrame - 08012020
    """
    Creates a pandas dataframe with transfer wait times and transfer values (TotalTransfers = TransDir + TransAlightWalk + TransWalkBorad)      
    """
    # Create the object and add required columns
    stopPointsList = Visum.Lists.CreateStopPointBaseList
    stopPointsList.AddColumn("No")
    stopPointsList.AddColumn("StopAreaNo")
    stopPointsList.AddColumn("NodeNo")
    stopPointsList.AddColumn("PassTransTotal(AP)")
    stopPointsList.AddColumn("PassTransDir(AP)")
    stopPointsList.AddColumn("PassTransWalkBoard(AP)")
    stopPointsList.AddColumn("PassTransAlightWalk(AP)")
    stopPointsList.AddColumn("TransferWaitTime(AP)")

    columnsList = ["No", "StopAreaNo", "NodeNo", "PassTransTotal(AP)", "PassTransDir(AP)", "PassTransWalkBoard(AP)",
                   "PassTransAlightWalk(AP)", "TransferWaitTime(AP)"]

    # creating pandas dataframe

    stopPointListArray = stopPointsList.SaveToArray()
    stopPointListDf = pd.DataFrame(list(stopPointListArray), columns=columnsList)

    return stopPointListDf


def createStopTransferWalkTimeDataFrame(Visum):
    visumTransferWalkTime = Visum.Lists.CreateStopTransferWalkTimeList
    visumTransferWalkTime.AddColumn("StopNo")
    visumTransferWalkTime.AddColumn("FromStopAreaNo")
    visumTransferWalkTime.AddColumn("ToStopAreaNo")
    visumTransferWalkTime.AddColumn("PassTransTotal(AP)")

    visumTransferWalkTimeArray = visumTransferWalkTime.SaveToArray()
    transferWalkTimeDf = pd.DataFrame(list(visumTransferWalkTimeArray),
                                      columns=["StopNo", "FromStopAreaNo", "ToStopAreaNo", "PassTransTotal(AP)"])

    return transferWalkTimeDf


def createConnectorListDataFrame(Visum):
    visumConnectors = Visum.Lists.CreateConnectorList
    visumConnectors.AddColumn("ZoneNo")
    visumConnectors.AddColumn("NodeNo")
    visumConnectors.AddColumn("Direction")
    visumConnectors.AddColumn("VolPersPuT(AP)")

    visumConnectorsArray = visumConnectors.SaveToArray()
    connectorsDf = pd.DataFrame(list(visumConnectorsArray), columns=["ZoneNo", "NodeNo", "Direction", "VolPersPuT(AP)"])

    return connectorsDf


def createLineRouteListDataFrame(Visum):
    visumLineRoutes = Visum.Lists.CreateLineRouteList
    visumLineRoutes.AddColumn("LineName")
    visumLineRoutes.AddColumn("Name")
    visumLineRoutes.AddColumn("DirectionCode")
    visumLineRoutes.AddColumn("PTripsUnlinked(AP)")
    visumLineRoutes.AddColumn("PTripsUnlinked0(AP)")
    visumLineRoutes.AddColumn("PTripsUnlinked1(AP)")
    visumLineRoutes.AddColumn("PTripsUnlinked2(AP)")
    visumLineRoutes.AddColumn("PTripsUnlinked>2(AP)")

    visumLineRoutesArray = visumLineRoutes.SaveToArray()
    lineRouteDf = pd.DataFrame(list(visumLineRoutesArray),
                               columns=["LineName", "Name", "DirectionCode", "PTripsUnlinked(AP)",
                                        "PTripsUnlinked0(AP)", "PTripsUnlinked1(AP)", "PTripsUnlinked2(AP)",
                                        "PTripsUnlinked>2(AP)"])

    return lineRouteDf


def createStopsListDataFrame(Visum):
    """
    created on 27022020
    create stop data frame
    created to use in singapore network
    """
    visumStops = Visum.Lists.CreateStopBaseList
    visumStops.AddColumn("No")
    visumStops.AddColumn("PassTransTotal(AP)")
    visumStops.AddColumn("PassTransDir(AP)")
    visumStops.AddColumn("PassTransWalkBoard(AP)")
    visumStops.AddColumn("PassTransAlightWalk(AP)")

    columnsList = ["No", "PassTransTotal(AP)", "PassTransDir(AP)", "PassTransWalkBoard(AP)",
                   "PassTransAlightWalk(AP)"]

    # creating pandas dataframe

    stopListArray = visumStops.SaveToArray()
    stopListDf = pd.DataFrame(list(stopListArray), columns=columnsList)

    return stopListDf


def getPuTStats(Visum):
    visumPuTStats = Visum.Lists.CreatePuTStatList
    visumPuTStats.AddColumn("PTripsLinkedWoCon")
    statsArray = visumPuTStats.SaveToArray()
    statList = list(statsArray)  # contain a list of tupels
    paxTripsWoCon_tup = statList[0]
    paxTripsWoCon = paxTripsWoCon_tup[0]

    return paxTripsWoCon
