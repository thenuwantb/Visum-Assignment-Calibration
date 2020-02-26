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

directory_path = "E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files"
# 1. Load the network
ver_file = "OriginalNetwork_DirectAssignment.ver"
version_path = os.path.join(directory_path, ver_file)
Visum = com.Dispatch("Visum.Visum.170")
ocv.loadVisum(VisumComDispatch=Visum, verPath=version_path)

# 2. Read in the list of origins and convert it to a list
origin_file = "E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files\\all_origins.csv"
# origin_file_major = "E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files\\origins_greater_than_100000.csv"

all_origins = pd.read_csv(origin_file)
all_origins_list = all_origins['NO'].to_list()

# sample_origins origin list will take less time to execute.  Good for testing
sample_origins = [3032002, 3030693, 3029040, 3029331, 3004970]

# filter_3_all = pd.DataFrame(columns=['OrigZoneNo', 'DestZoneNo', 'Index', 'ODTrips', 'NumTransfers', 'InVehDist'])
filter_3_all = pd.DataFrame()
min_route_share = pd.DataFrame(columns=['OrigZoneNo', 'DestZoneNo', 'MinRouteTrips', 'TotalODTrips', 'MinSharePEC'])

# range(len(all_origins_list))
for origin_zone in range(len(sample_origins)):
    print origin_zone
    # Create PuTPaths object with 'OrigZoneNo', 'DestZoneNo', 'Index', 'ODTrips', 'NumTransfers', 'InVehDist'
    put_paths = Visum.Lists.CreatePuTPathList
    put_paths.AddColumn('OrigZoneNo')
    put_paths.AddColumn('DestZoneNo')
    put_paths.AddColumn('Index')
    put_paths.AddColumn('ODTrips')
    put_paths.AddColumn('NumTransfers')
    put_paths.AddColumn('InVehDist')

    # filter from the origin zone number
    put_paths.SetObjects(Zone=sample_origins[origin_zone], DemandSeg="X", PathTypeSelection=0)

    # chunks and write
    # num_lines = put_paths.NumActiveElements
    # chunk_size = 100000

    # if num_lines > chunk_size:
    #     put_paths_df = pd.DataFrame(
    #         columns=['OrigZoneNo', 'DestZoneNo', 'Index', 'ODTrips', 'NumTransfers', 'InVehDist'])
    #     for i in range(num_lines / chunk_size + 1):
    #         put_paths_array_chunk = put_paths.SaveToArray(fromRow=i * chunk_size + 1, toRow=(i + 1) * chunk_size)
    #         array_to_list_chunk = list(put_paths_array_chunk)
    #         interim_chunk_df = pd.DataFrame(array_to_list_chunk)
    #         put_paths_df = put_paths_df.append(interim_chunk_df, ignore_index=True)
    #
    # else:
    #     put_paths_array = put_paths.SaveToArray(fromRow=1, toRow=-1)
    #     put_paths_df = pd.DataFrame(list(put_paths_array),
    #                                 columns=['OrigZoneNo', 'DestZoneNo', 'Index', 'ODTrips', 'NumTransfers',
    #                                          'InVehDist'])
    put_paths_array = put_paths.SaveToArray(fromRow=1, toRow=-1)
    put_paths_df = pd.DataFrame(list(put_paths_array),
                                columns=['OrigZoneNo', 'DestZoneNo', 'Index', 'ODTrips', 'NumTransfers', 'InVehDist'])

    n_rows, n_cols = put_paths_df.shape
    if n_rows == 0:
        continue

    per_route_sum_df = put_paths_df.groupby(['OrigZoneNo', 'DestZoneNo', 'NumTransfers', 'InVehDist'])[
        'ODTrips'].sum().to_frame().reset_index()
    per_od_sum_df = per_route_sum_df.groupby(['OrigZoneNo', 'DestZoneNo'])['ODTrips'].sum().to_frame().reset_index()
    route_share_df = per_route_sum_df.merge(per_od_sum_df, on=['OrigZoneNo', 'DestZoneNo'])
    change_col = {'ODTrips_x': 'RouteODTrips', 'ODTrips_y': 'TotalODTrips'}
    route_share_df = route_share_df.rename(columns=change_col)

    # calculate route share
    route_share_df['RouteSharePEC'] = (route_share_df['RouteODTrips'] / route_share_df['TotalODTrips']) * 100

    # for the purpose of this calculation, certain insignificant records need to filter out
    # 1. Filter out minor OD flows
    total_od_greater_10 = route_share_df['TotalODTrips'] >= 10
    filter1_df = route_share_df[total_od_greater_10]

    # 2. if any of the route in a given OD pair has a route share > 90%, it means that that route is the dominated
    # route and most likely rest of the routes are non-dominant routes # if such OD pairs exists, those OD pairs have
    # to be removed entirely from the data set

    filter2_df = filter1_df.copy().groupby(['OrigZoneNo', 'DestZoneNo']).filter(
        lambda _group: _group['RouteSharePEC'].max() < 99)

    # 3. OD paths with the minimum route od trips = 10 (less than 1 trip per day) trip is also removed

    filter3_df = filter2_df.copy().groupby(['OrigZoneNo', 'DestZoneNo']).filter(
        lambda _group: _group['RouteODTrips'].min() >= 10)

    # 3.1. write all data from filter 3 to a new dataframe and save it after the for loop
    filter_3_all = filter_3_all.append(filter3_df, ignore_index=True)

    # 4. Write minimum route share per OD pair (min_route_share = pd.DataFrame(columns=['OrigZoneNo', 'DestZoneNo',
    # 'MinSharePEC'])

    for od_pair, group in filter3_df.groupby(['OrigZoneNo', 'DestZoneNo']):
        origin, destination = od_pair

        group_min_pec = group['RouteSharePEC'].min()
        total_od_trips = group['TotalODTrips'].mean()
        min_route_trips = group['RouteODTrips'].min()

        # 'OrigZoneNo', 'DestZoneNo', 'MinRouteTrips', 'TotalODTrips', 'MinSharePEC']
        min_route_share = min_route_share.append(
            {'OrigZoneNo': origin, 'DestZoneNo': destination, 'MinRouteTrips': min_route_trips,
             'TotalODTrips': total_od_trips, 'MinSharePEC': group_min_pec}, ignore_index=True)

min_route_share.to_csv("E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files\\s_min_route_share_99_26022020.csv")
filter_3_all.to_csv(
    "E:\\Thenuwan\\DirectAssignment-10 days\\Visum Files\\s_min_route_share_99_filter_3_all_26022020.csv")
