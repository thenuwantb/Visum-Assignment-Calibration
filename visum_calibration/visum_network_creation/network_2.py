'''
Created on 6 Jan 2020

@author: thenuwan.jayasinghe
'''
import sys
import os.path
import win32com.client as com
import datetime 
import pandas as pd
import numpy as np
import timeit
from win32con import EN_STOPNOUNDO

#Load Visum Version and Create a Network Object
path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\02_Network"
verFile = "1_Blank.ver"
versionPath =  os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")
Visum.LoadVersion(versionPath)

Net = Visum.Net

linktype20 = Net.AddLinkType(20)
linktype20.SetAttValue("TSYSSET", "B")


#The aim is to add Zones, nodes, links and connectors. Rest of the changes area done within Visum itself

#Add Zones
zoneData =  pd.read_csv(os.path.join(path, "Zones.csv"))
for index, row in zoneData.iterrows():
    
    no = row['no']
    name = row['name']
    XCoord = row['XCoord']
    YCoord = row['YCoord']
    
    zone = Net.AddZone(no)
    zone.SetAttValue("NAME", str(name))
    zone.SetAttValue("XCOORD", str(XCoord))
    zone.SetAttValue("YCOORD", str(YCoord))

#Add Nodes
nodeData = pd.read_csv(os.path.join(path, "Nodes.csv"))
for index, row in nodeData.iterrows():
    no = row['no']
    xCoord = row['XCoord']
    yCoord = row['YCoord']
     
    Net.AddNode(no, xCoord, yCoord)

#Add Connectors
connectorsData = pd.read_csv(os.path.join(path, "Connectors.csv"))
for index, row in connectorsData.iterrows():
    
    zone = int(row['zone'])
    node = int(row['node'])
    
    Net.AddConnector(zone, node)
    
#Add Links

linkData = pd.read_csv(os.path.join(path, "Links.csv"))
for index, row in linkData.iterrows():
    fromNode = int(row['fromNode'])
    toNode = int(row['toNode'])
    linkType = int(row['linkType'])
    
    Net.AddLink(-1, fromNode, toNode, linkType)
    
#Add Stop related data
stopFilePath = os.path.join(path, "Stops.xlsx")

print stopFilePath
stopData = pd.read_excel(stopFilePath, 'stops')
stopAreaData = pd.read_excel(stopFilePath, 'stopAreas')
stopPointsOnNodeData = pd.read_excel(stopFilePath, 'stopPointsOnNodes')

##Add Stops
for index, row in stopData.iterrows():
    no = int(row['no'])
    stopName = str(row['stopName'])
    XCoord = int(row['XCoord'])
    YCoord = int(row['YCoord'])
    
    stop = Net.AddStop(no, XCoord, YCoord)
    stop.SetAttValue("NAME", stopName)
    
##Add Stop Areas
for index, row in stopAreaData.iterrows():
    no = int(row['no'])
    stop = int(row['stop'])
    node = int(row['node'])
    xCoord = int(row['XCoord'])
    yCoord = int(row['YCoord'])
    
    Net.AddStopArea(no, stop, node, xCoord, yCoord)
    
##Add Stop Points on Node
for index, row in stopPointsOnNodeData.iterrows():
    no = int(row['no'])
    stopArea = int(row['stopArea'])
    node = int(row['node'])
    
    Net.AddStopPointOnNode(no, stopArea, node)

#Change List - Transfers and walktimes within stop : calculate walk time with a speed of 1km /h

visumTransferWalkTime = Visum.Lists.CreateStopTransferWalkTimeList
visumTransferWalkTime.AddColumn("StopNo")
visumTransferWalkTime.AddColumn("FromStopAreaNo")
visumTransferWalkTime.AddColumn("ToStopAreaNo")
visumTransferWalkTime.AddColumn("DirectDist")
visumTransferWalkTime.AddColumn("Time(W)")

visumTransferWalkTimeArray = visumTransferWalkTime.SaveToArray()

transferWalkTimeDf = pd.DataFrame(list(visumTransferWalkTimeArray), columns = ["StopNo", "FromStopAreaNo","ToStopAreaNo","DirectDist","Time(W)"])

allStops = Visum.Net.Stops.GetAll


for index, row in transferWalkTimeDf.iterrows():
    stopNo = int(row['StopNo'])
    fromStopArea = int(row['FromStopAreaNo'])
    toStopArea = int(row['ToStopAreaNo'])
    directDistance = row['DirectDist']
    
    distanceInMeters = directDistance * 1000
    #walk speed is assumed to 1 meters per second
    speed = 1.0
    walkingTime = distanceInMeters / speed  #walking time in seconds
    
    currentStop = allStops[stopNo-1]
    
    #set walking time
    currentStop.SetStopAreaTransferWalkTime(fromStopArea, toStopArea, 'W', walkingTime)
    
#-------------------------End Main Code-----------------------------------------------------

#Write the new Version file
fileName, ext = os.path.splitext(versionPath)
saveAs = "Network_2" + "_" + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M") + ext
saveFileTo = os.path.join(os.path.dirname(versionPath), saveAs)
Visum.SaveVersion(saveFileTo)
