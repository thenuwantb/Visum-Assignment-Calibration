'''
Created on 9 Dec 2019

@author: thenuwan.jayasinghe
'''
import math


def calculateRMSN (observedList, simulatedList):
    
    differenceList = [obs_i - sim_i for obs_i, sim_i in zip(observedList, simulatedList)]
    differenceSquared = [diff**2 for diff in differenceList]
    
    sumOfDifferenceSquared = sum(differenceSquared)
    sumOfObserved = sum(observedList)
    
    rmsn = (math.sqrt(len(observedList) * sumOfDifferenceSquared)) / sumOfObserved
    
    return rmsn
    