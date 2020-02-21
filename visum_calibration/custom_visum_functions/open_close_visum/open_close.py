'''
Created on 2 Dec 2019

@author: thenuwan.jayasinghe
'''
import os

import win32com.client as com


def loadVisum(VisumComDispatch, verPath):
    VisumComDispatch.LoadVersion(verPath)
