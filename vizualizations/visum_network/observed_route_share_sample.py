'''
Created on 17 Feb 2020

@author: thenuwan.jayasinghe
@note: script calculates the %of trips on different routes for the origing destination of 3004904 (Trips originated from STN Aljunied)
'''

import pandas as pd
import matplotlib.pyplot as plt

col_names  = ['ORIGZONENO','DESTZONENO','INDEX','ODTRIPS','NUMTRANSFERS','INVEHDIST']
path = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\sampel_PuT_Paths_O3004925_17022020.csv"
data = pd.read_csv(path, header = None, names = col_names)
 
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
 
total_merged_df = unique_route_sum.merge(trip_sum_per_odpair, on = ['ORIGZONENO', 'DESTZONENO'])
change_col_total_merged = {'ODTRIPS_x' : 'ROUTE_OD',  'ODTRIPS_y':'TOTAL_OD' }
total_merged_df = total_merged_df.rename(columns = change_col_total_merged)
 
total_merged_df['SHARE(%)'] = (total_merged_df['ROUTE_OD'] / total_merged_df['TOTAL_OD'])*100
 
 
filter_4 = total_merged_df['DESTZONENO'] == 3003190
 
print total_merged_df[filter_4]
 
save_resuls = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\sample_results_18022020.csv"
  
total_merged_df.to_csv(save_resuls)
  
total_merged_df.hist(column = 'SHARE(%)', bins = 100)
plt.show()


# 1. removing OD pairs < 10 trips
data_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\sample_results_18022020.csv")

total_od_greater_10 = data_df['TOTAL_OD'] >= 10

data_od_greater_10_df = data_df[total_od_greater_10]
data_od_greater_10_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\df1.csv")
#===============================================================================
# data_od_greater_10_df['SHARE(%)'].hist(bins =100)
# plt.show()
#===============================================================================


# 2. if any of the route in a given OD pair has a route share > 90%, it means that that route is the dominated route and most likely rest of the routes are non-dominant routes
# if such OD pairs exists, those OD pairs have to be removed entirely from the data set

data_od_90 = data_od_greater_10_df.copy()
data_od_90_groupby = data_od_90.groupby(['ORIGZONENO', 'DESTZONENO'])


data_od_90_groupby_df = data_od_90_groupby.filter(lambda group : group['SHARE(%)'].max() < 90) 
#data_od_90_groupby_df .to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\df3.csv")   

#===============================================================================
# data_od_90_groupby_df['SHARE(%)'].hist(bins =100)
# plt.show()
#===============================================================================

# 3. OD paths with the minimum route od trips = 10 (less than 1 trip per day) trip is also removed

data_remove_1_OD = data_od_90_groupby_df.copy()
data_remove_1_OD_groupby = data_remove_1_OD.groupby(['ORIGZONENO', 'DESTZONENO'])
data_remove_1_OD_df = data_remove_1_OD_groupby.filter(lambda group : group['ROUTE_OD'].min() >= 10)
#data_remove_1_OD_df .to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\df5.csv") 

data_remove_1_OD_df['SHARE(%)'].hist(bins =100)
plt.show()





        
    



