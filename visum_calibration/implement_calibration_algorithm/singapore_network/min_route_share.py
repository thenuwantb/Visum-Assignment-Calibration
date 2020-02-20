'''
Created on 20 Feb 2020

@author: thenuwan.jayasinghe
@note : iterate over all the origins of direct assignment visum file's PuT paths and calculate a value for the minimum route share %
'''

import sys
import os
import win32com.client as com
import pandas as pd
from custom_visum_functions.open_close_visum import open_close as ocv


path = "E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files"
verFile = "OriginalNetwork_DirectAssignment.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.170")

ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)


