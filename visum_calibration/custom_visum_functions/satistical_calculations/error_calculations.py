"""
Created on 9 Dec 2019

@author: thenuwan.jayasinghe
"""
import math


def calculate_rmsn(observedList, simulatedList):
    differenceList = [obs_i - sim_i for obs_i, sim_i in zip(observedList, simulatedList)]
    differenceSquared = [diff ** 2 for diff in differenceList]

    sumOfDifferenceSquared = sum(differenceSquared)
    sumOfObserved = sum(observedList)

    rmsn = (math.sqrt(len(observedList) * sumOfDifferenceSquared)) / sumOfObserved

    return rmsn


def calculate_rmsn_0(observed, simulated):
    count = 0
    error = 0
    diff_squared_sum = 0
    sum_obs = 0

    for obs_i, sim_i in zip(observed, simulated):
        if obs_i > 0:
            diff_squared_sum += (obs_i - sim_i) ** 2
            sum_obs += obs_i
            count += 1
        else:
            continue
    rmsn_error_0 = math.sqrt(count*diff_squared_sum)/sum_obs
    return  rmsn_error_0

def calculate_mape(observed, simulated):
    count = 0
    error = 0
    for obs_i, sim_i in zip(observed, simulated):
        if obs_i > 0:
            error += abs((obs_i - sim_i) / obs_i)
            count += 1
        else:
            continue
    mape_error = error / count
    return mape_error


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

    return rmspe


def calculateABS(observedList, simulatedList):
    differenceList = [abs(sim_i - obs_i) for obs_i, sim_i in zip(observedList, simulatedList)]
    differenceListDivObs = [diff_i / obs_i if obs_i != 0 else 0 for diff_i, obs_i in zip(differenceList, observedList)]
    sumOfDifferenceList = sum(differenceListDivObs)

    return sumOfDifferenceList
