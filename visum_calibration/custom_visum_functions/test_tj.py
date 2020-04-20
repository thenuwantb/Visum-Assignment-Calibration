import pandas as pd

obs_data = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\test\\Dir_LINEROUTE.csv")
sim_data = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\test\\LINEROUTE_lines_removed.csv")

line_routes_merged = pd.merge(sim_data, obs_data, on=['LINENAME', 'NAME'], how='left', suffixes=['_SIM', '_OBS'])

line_routes_merged.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\test\\output.csv")
