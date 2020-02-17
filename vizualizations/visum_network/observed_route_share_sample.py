'''
Created on 17 Feb 2020

@author: thenuwan.jayasinghe
@note: script calculates the %of trips on different routes for the origing destination of 3004904 (Trips originated from STN Aljunied)
'''

import pandas as pd

col_names  = ['ORIGZONENO','DESTZONENO','INDEX','ODTRIPS','NUMTRANSFERS','INVEHDIST']
data = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\sampel_PuT_Paths_O3004925_17022020.csv", header = None, names = col_names)

filter_1 = data['DESTZONENO'] == 3003190
#print data[filter_1]
#===============================================================================
#     ORIGZONENO  DESTZONENO  INDEX  ODTRIPS  NUMTRANSFERS  INVEHDIST
# 0      3004925     3003190      1      1.0           1.0      22.97
# 1      3004925     3003190      2      1.0           3.0      24.43
# 2      3004925     3003190      3      1.0           1.0      22.97
# 3      3004925     3003190      4      1.0           1.0      22.97
# 4      3004925     3003190      5      1.0           1.0      30.18
# 5      3004925     3003190      6      1.0           1.0      22.63
# 6      3004925     3003190      7      1.0           1.0      22.63
# 7      3004925     3003190      8      1.0           1.0      22.97
# 8      3004925     3003190      9      1.0           1.0      22.97
# 9      3004925     3003190     10      1.0           1.0      22.63
# 10     3004925     3003190     11      1.0           1.0      22.97
#===============================================================================
#sample1 =data.groupby(['ORIGZONENO', 'DESTZONENO'])['ODTRIPS'].sum().to_frame().reset_index() #works

unique_route_sum = data.groupby(['ORIGZONENO', 'DESTZONENO', 'NUMTRANSFERS', 'INVEHDIST'])['ODTRIPS'].sum().to_frame().reset_index()

filter_2 = unique_route_sum['DESTZONENO'] == 3003190

#print unique_route_sum[filter_2]
#===============================================================================
#    ORIGZONENO  DESTZONENO  NUMTRANSFERS  INVEHDIST  ODTRIPS
# 0     3004925     3003190           1.0      22.63      3.0
# 1     3004925     3003190           1.0      22.97      6.0
# 2     3004925     3003190           1.0      30.18      1.0
# 3     3004925     3003190           3.0      24.43      1.0
#===============================================================================

trip_sum_per_odpair = data.groupby(['ORIGZONENO', 'DESTZONENO'])['ODTRIPS'].sum().to_frame().reset_index()
filter_3 = trip_sum_per_odpair['DESTZONENO'] == 3003190

#print trip_sum_per_odpair[filter_3]

#===============================================================================
#    ORIGZONENO  DESTZONENO  ODTRIPS
# 0     3004925     3003190     11.0
#===============================================================================

unique_route_sum_merge_total = unique_route_sum.merge(trip_sum_per_odpair, on = ['ORIGZONENO', 'DESTZONENO'])
filter_4 = unique_route_sum_merge_total['DESTZONENO'] == 3003190

print unique_route_sum_merge_total[filter_4]


