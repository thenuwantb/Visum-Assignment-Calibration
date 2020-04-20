'''
Created on 26 Feb 2020

@author: thenuwan.jayasinghe
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
#data_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\2_Presentations\\8_Update_to_Dr_Rau_26022020\\min_route_share_99_26022020.csv")
data_df= pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\2_Presentations\\8_Update_to_Dr_Rau_26022020\\min_route_share_99_rounded26022020.csv")
#data_df = pd.read_csv("E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files\\min_route_share_99_26022020.csv")

od_total_threshold = 0
min_route_trip_threshold = 0
od_total_filter = (data_df['TotalODTrips'] >= od_total_threshold) & (data_df['MinShareRoundPEC'] >= min_route_trip_threshold)

od_filter_df = data_df[od_total_filter]

#visualization
#===============================================================================
# bins = range(100)
# min_route_pec_list = od_filter_df['MinShareRoundPEC'].tolist()
# _ = plt.hist(min_route_pec_list, bins =100, edgecolor = 'black', cumulative=True)
# _ = plt.xticks(list(range(50)))
# _ = plt.xlabel("Minimum route share %")
# _ = plt.ylabel("Count")
# _ = plt.title("Minimum route share distribution")
#===============================================================================


#===============================================================================
# # remove the binning bias
# x = np.sort(od_filter_df['MinShareRoundPEC'])
# y = np.arange(1, len(x)+1) / len(x)
# _ = plt.plot(x,y, marker = '.', linestyle='none')
#===============================================================================


min_route_pec_list = od_filter_df['MinSharePEC'].tolist()
fig, ax = plt.subplots()
ax.hist(min_route_pec_list, density=False, bins = 100, histtype='stepfilled', align='mid', color='lightgrey', edgecolor='black')
ax.set_xlabel("Minimum route share (%)", fontsize=8)
ax.set_ylabel("Count", fontsize=8)
ax.set_title("Distribution of minimum route share %", fontsize=10)
ax.set_xticks(list(np.arange(0,55,5)))
ax.axvline(x=4.75, color = 'red', linestyle = '--')

plt.savefig("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\4_Report\\plots\\min_route_share\\with_4_75_avline.svg")

#plt.show()


# plt.show()
