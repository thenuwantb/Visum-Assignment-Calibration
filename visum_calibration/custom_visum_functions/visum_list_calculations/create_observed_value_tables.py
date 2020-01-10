'''
Created on 7 Jan 2020

@author: thenuwan.jayasinghe
@note: Created the script with the intention of creating observed data points from Visum (this has to be done prior to run the algorithms)
'''
import os.path
import win32com.client as com
from custom_visum_functions.open_close_visum import open_close as ocv

import pandas as pd
from custom_visum_functions.visum_list_calculations import list_calculations as lc

path = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network"
verFile = "Network_2_20200107_TJ_Final.ver"
versionPath = os.path.join(path, verFile)
Visum = com.Dispatch("Visum.Visum.180")

#save results 
observed_data_save_as = "C:\\Users\\thenuwan.jayasinghe\\Documents\\_Thesis\\Coding\\Experiments\\07012020\\network\\stop_point_total_pax_transfer_observed_10012020.csv"

# load Visum file
ocv.loadVisum(VisumComDispatch=Visum, verPath=versionPath)

observed_df = lc.createStopPointsDataFrame(Visum)
observed_df.to_csv(observed_data_save_as,  index = False)