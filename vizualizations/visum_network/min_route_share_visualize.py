'''
Created on 26 Feb 2020

@author: thenuwan.jayasinghe
'''

import pandas as pd
import matplotlib.pyplot as plt

data_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\2_Presentations\\8_Update_to_Dr_Rau_26022020\\min_route_share_99_26022020.csv")

od_total_threshold = 10
od_total_filter = data_df['TotalODTrips'] >= od_total_threshold

od_filter_df = data_df[od_total_filter]

#visualization

min_route_pec_list = od_filter_df['MinSharePEC'].tolist()
_ = plt.hist(min_route_pec_list, bins = 50)
plt.show()
