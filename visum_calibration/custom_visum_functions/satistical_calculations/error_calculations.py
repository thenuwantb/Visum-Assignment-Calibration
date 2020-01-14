'''
Created on 9 Dec 2019

@author: thenuwan.jayasinghe
'''
import math


def calculateRMSN (observedList, simulatedList):
    
    differenceList = [obs_i - sim_i for obs_i, sim_i in zip(observedList, simulatedList)]
    differenceSquared = [diff ** 2 for diff in differenceList]
    
    sumOfDifferenceSquared = sum(differenceSquared)
    sumOfObserved = sum(observedList)
    
    rmsn = (math.sqrt(len(observedList) * sumOfDifferenceSquared)) / sumOfObserved
    
    return rmsn


def calculateRMPSE(observedList, simulatedList):
    """
    Root Mean Square Percentage Error penalized large error more heavily than small errors 
    http://dx.doi.org/10.1016/j.trc.2015.02.016
    """
    differenceList = [sim_i - obs_i for obs_i, sim_i in zip(observedList, simulatedList)]
    differenceListDivObs = [diff_i / obs_i if obs_i != 0 else 0 for diff_i, obs_i in zip(differenceList, observedList)]
    # print differenceListDivObs
    differenceSquared = [diff ** 2 for diff in differenceListDivObs]
    
    sumOfDifferenceSquared = sum(differenceSquared)
    
    rmspe = math.sqrt(sumOfDifferenceSquared / len(differenceSquared))
    # print rmspe
    
    return rmspe
    
