'''
Created on 19 Feb 2020

@author: thenuwan.jayasinghe
@note : I wanted to make sure that the Direct assignment model and the headway-based simulation model are in same temporal scale, so that it is made sure that the error term calculated is make sense
'''

import pandas as pd
import matplotlib.pyplot as plt

data_df = pd.read_excel(
    "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Manual Calibration\\Stops Data\\Stops\\stops_AP_level_analysis_19022020_hist.xlsx")

# ===============================================================================
# Index([u'NO', u'CODE', u'NAME', u'PASSORIGIN(AP)_1', u'PASSDESTINATION(AP)_1',
#        u'PASSORIGIN(AP)_10', u'PASSDESTINATION(AP)_10'],
#       dtype='object')
# ===============================================================================

data_df.boxplot(column=['PASSORIGIN(AP)_1', 'PASSDESTINATION(AP)_1'], showfliers=False)
# data_df.boxplot(column = ['PASSORIGIN(AP)_10','PASSDESTINATION(AP)_10'] , showfliers=False)
plt.show()
