'''
Created on 19 Feb 2020

@author: thenuwan.jayasinghe
'''
import pandas as pd
import matplotlib.pyplot as plt

# ===============================================================================
# col_names  = ['ORIGZONENO','DESTZONENO','INDEX','ODTRIPS','NUMTRANSFERS','INVEHDIST']
# path = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\Major_origns\\3004925_Raffles_place.csv"
# 
# data_df = pd.read_csv(filepath_or_buffer = path, header = None, names = col_names)
# print data_df.head()
# 
# per_route_sum = data_df.groupby(['ORIGZONENO', 'DESTZONENO', 'NUMTRANSFERS', 'INVEHDIST'])['ODTRIPS'].sum().to_frame().reset_index()
# per_od_sum = data_df.groupby(['ORIGZONENO', 'DESTZONENO'])['ODTRIPS'].sum().to_frame().reset_index()
# print per_od_sum.head()
# 
# route_share_df = per_route_sum.merge(per_od_sum, on = ['ORIGZONENO', 'DESTZONENO'])
# change_col = {'ODTRIPS_x' : 'ROUTE_OD',  'ODTRIPS_y':'TOTAL_OD' }
# route_share_df = route_share_df.rename(columns = change_col)
# 
# #calculate route share
# route_share_df['SHARE(%)'] = (route_share_df['ROUTE_OD'] / route_share_df['TOTAL_OD'])*100
# print route_share_df.head()
# 
# #filtering
# ## 1. Filter out minor OD flows
# total_od_greater_10 = route_share_df['TOTAL_OD'] >= 10
# filter1_df = route_share_df[total_od_greater_10]
# print filter1_df.head()
# 
# ##2. if any of the route in a given OD pair has a route share > 90%, it means that that route is the dominated route and most likely rest of the routes are non-dominant routes
# ## if such OD pairs exists, those OD pairs have to be removed entirely from the data set
# 
# filter2_df = filter1_df.copy().groupby(['ORIGZONENO', 'DESTZONENO']).filter(lambda group : group['SHARE(%)'].max() < 90)
# 
# ## 3. OD paths with the minimum route od trips = 10 (less than 1 trip per day) trip is also removed
# 
# filter3_df = filter2_df.copy().groupby(['ORIGZONENO', 'DESTZONENO']).filter(lambda group : group['ROUTE_OD'].min() >= 10)
# print filter3_df.head()
# 
# # minimum route share per OD pair
# min_route_share = pd.DataFrame(columns=['Origin', 'Destination', 'Min_Share(%)'])
# for od_pair, group in filter3_df.groupby(['ORIGZONENO', 'DESTZONENO']):
#     origin, destination = od_pair
#     group_min = group['SHARE(%)'].min()
#     
#     min_route_share = min_route_share.append({'Origin': origin, 'Destination': destination, 'Min_Share(%)' :group_min}, ignore_index = True)
#     
# print min_route_share.head()
#     
# 
# #===============================================================================
# # #save results
# # save_path = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\Direct Assignment\\Major_origns\\3004925_Raffles_place_cleaned.csv"
# # filter3_df.to_csv(save_path)
# # 
# # filter3_df['SHARE(%)'].hist(bins = 100)
# # plt.show()
# #===============================================================================
# ===============================================================================

data = pd.read_csv(
    "E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files\\min_route_share_99_24022020.csv")

data['MinSharePEC'].hist(bins=100)
#data['MinSharePEC'].hist(cumulative=True, density = 1, bins = 100)
plt.show()
