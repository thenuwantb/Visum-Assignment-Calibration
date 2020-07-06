import pandas as pd
import numpy as np

df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\Discussion with Moeid\\Final model error\\mape_test\\calibrated_model_obs_sim_stops_06072020.csv")

pax_trans_total_obs = df['PASSTRANSTOTAL(AP)_OBS'].tolist()
pax_trans_total_sim = df['PASSTRANSTOTAL(AP)_SIM'].tolist()

pax_trans_dir_obs = df['PASSTRANSDIR(AP)_OBS'].tolist()
pax_trans_dir_sim = df['PASSTRANSDIR(AP)_SIM'].tolist()

pax_trans_walkb_obs = df['PASSTRANSWALKBOARD(AP)_OBS'].tolist()
pax_trans_walkb_sim = df['PASSTRANSWALKBOARD(AP)_SIM'].tolist()

pax_trans_alightw_obs = df['PASSTRANSALIGHTWALK(AP)_OBS'].tolist()
pax_trans_alightw_sim = df['PASSTRANSALIGHTWALK(AP)_SIM'].tolist()

def calculate_mape(observed, simulated):
    # mape_error = 0
    count = 0
    error = 0
    for obs_i, sim_i in zip(observed, simulated):
        if obs_i > 0:
            error += abs((obs_i - sim_i) / obs_i)
            count += 1
        else:
            continue
    mape_error = error / count
    return mape_error

mape_total =calculate_mape(pax_trans_total_obs, pax_trans_total_sim)
mape_dir = calculate_mape(pax_trans_dir_obs, pax_trans_dir_sim)
mape_alightw = calculate_mape(pax_trans_alightw_obs, pax_trans_alightw_sim)
mape_walkb = calculate_mape(pax_trans_walkb_obs, pax_trans_walkb_sim)

print mape_total
print mape_dir
print mape_alightw
print mape_walkb

