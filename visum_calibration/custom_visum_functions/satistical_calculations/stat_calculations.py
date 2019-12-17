'''
Created on 9 Dec 2019

@author: thenuwan.jayasinghe
'''
import math


def calculateRMSN (observedList, simulatedList):
    '''Based on equation 13 PC-SPSA paper'''
    differenceList = [obs_i - sim_i for obs_i, sim_i in zip(observedList, simulatedList)]
    differenceSquared = [diff**2 for diff in differenceList]
    
    sumOfDifferenceSquared = sum(differenceSquared)
    sumOfObserved = sum(observedList)
    
    RMSN = (math.sqrt(len(observedList) * sumOfDifferenceSquared)) / sumOfObserved
    
    return RMSN
    