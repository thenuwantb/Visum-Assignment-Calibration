import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import polyfit
from matplotlib.ticker import FuncFormatter

plt.style.use('seaborn-ticks')  # seaborn-white, ggplot


def add_gridline(axis):
    axis.grid(linestyle=':', linewidth=0.5, color='darkgray')


def thousands(x, pos):
    'The two args are the value and tick position'
    return '%1.0f' % (x * 1e-3)


# function to calculate r-squared and for plotting
def cal_r_squared(obs_list_x, sim_list_y):
    corr_mat = np.corrcoef(obs_list_x, sim_list_y)
    corr_xy = corr_mat[0, 1]
    r_squared = corr_xy ** 2
    return round(r_squared, 3)


def add_gridline(axis):
    axis.grid(linestyle=':', linewidth=0.5, color='darkgray')


def scatter_plot_axis(axis, obs_pd_series, sim_pd_series, color):
    axis.scatter(obs_pd_series, sim_pd_series,
                 alpha=0.8, color=color, s=scatter_size, edgecolors='none')
    axis.xaxis.set_major_locator(plt.MaxNLocator(6))
    axis.yaxis.set_major_locator(plt.MaxNLocator(6))

    axis_max = max(max(obs_pd_series),
                   max(sim_pd_series))
    axis.set(xlim=(0, axis_max + axis_max * 0.05), ylim=(0, axis_max + axis_max * 0.05))
    axis_max_list = list(np.arange(0, axis_max, int(axis_max / 20)))
    axis.plot(axis_max_list, axis_max_list, linestyle=':',
              color='dimgray', alpha=0.7)
    _b, _m = polyfit(obs_pd_series,
                     sim_pd_series, 1)
    _r = cal_r_squared(obs_pd_series.tolist(),
                       sim_pd_series.tolist())
    # ax1.plot(ax1_max_list, pd.Series(ax1_max_list)*m1 +b1, linestyle=':',color = 'k', alpha = 0.6)
    _bf = "{:.2f}".format(_b)
    _mf = "{:.2f}".format(_m)
    if _b < 0:
        axis.text(axis_max * reg_line_x, axis_max * reg_line_y,
                  "y = " + "{:.2f}".format(_m) + "x - " + "{:.2f}".format(abs(_b)), fontsize=7)
    else:
        axis.text(axis_max * reg_line_x, axis_max * reg_line_y,
                  "y = " + "{:.2f}".format(_m) + "x + " + "{:.2f}".format(abs(_b)), fontsize=7)
    axis.text(axis_max * r_2_x, axis_max * r_2_y, "$r^2$ = " + str(_r), fontsize=7)
    add_gridline(axis)

    x_0, x_1 = axis.get_xlim()
    y_0, y_1 = axis.get_ylim()
    axis.set_aspect(abs(x_1 - x_0) / abs(y_1 - y_0))

reg_line_x2 = 0.055
reg_line_y2 = 0.85
r_2_x2 = 0.03
r_2_y2 = 0.75

def scatter_plot_axis_2(axis, obs_pd_series, sim_pd_series, color):
    #plt.rc('figure', figsize=(8.27, 10))
    axis.scatter(obs_pd_series, sim_pd_series,
                 alpha=0.8, color=color, s=scatter_size, edgecolors='none')
    axis.xaxis.set_major_locator(plt.MaxNLocator(6))
    axis.yaxis.set_major_locator(plt.MaxNLocator(6))

    axis_max = max(max(obs_pd_series),
                   max(sim_pd_series))
    axis.set(xlim=(0, axis_max + axis_max * 0.05), ylim=(0, axis_max + axis_max * 0.05))
    axis_max_list = list(np.arange(0, axis_max, int(axis_max / 20)))
    axis.plot(axis_max_list, axis_max_list, linestyle=':',
              color='dimgray', alpha=0.7)
    _b, _m = polyfit(obs_pd_series,
                     sim_pd_series, 1)
    _r = cal_r_squared(obs_pd_series.tolist(),
                       sim_pd_series.tolist())
    # ax1.plot(ax1_max_list, pd.Series(ax1_max_list)*m1 +b1, linestyle=':',color = 'k', alpha = 0.6)
    _bf = "{:.2f}".format(_b)
    _mf = "{:.2f}".format(_m)
    if _b < 0:
        axis.text(axis_max * reg_line_x2, axis_max * reg_line_y2,
                  "y = " + "{:.2f}".format(_m) + "x - " + "{:.2f}".format(abs(_b)), fontsize=6.5)
    else:
        axis.text(axis_max * reg_line_x2, axis_max * reg_line_y2,
                  "y = " + "{:.2f}".format(_m) + "x + " + "{:.2f}".format(abs(_b)), fontsize=6.5)
    axis.text(axis_max * r_2_x2, axis_max * r_2_y2, "$r^2$ = " + str(_r), fontsize=6.5)
    add_gridline(axis)
    x_0, x_1 = axis.get_xlim()
    y_0, y_1 = axis.get_ylim()
    axis.set_aspect(abs(x_1 - x_0) / abs(y_1 - y_0))

    #reducing thickness
    axis.spines['top'].set_linewidth(0.75)
    axis.spines['right'].set_linewidth(0.75)
    axis.spines['bottom'].set_linewidth(0.75)
    axis.spines['left'].set_linewidth(0.75)

    axis.tick_params(width = 0.75)


# plot constant
subplot_title_size = 8
scatter_size = 25
scatter_color_vd = 'grey'
scatter_color_ig = 'orangered'
scatter_color_cal = 'royalblue'

plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('figure', figsize=(8.27, 8.5))  # 11.69
#plt.rc('figure', figsize=(5.5, 8.5))

# plotting positions
reg_line_x = 0.055 #0.57
reg_line_y = 0.85 #0.2
r_2_x = 0.03 # 0.55
r_2_y = 0.75 # 0.1

# observed data : permenant links
stops_obs_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\obs_stops_04032020.csv")
line_route_obs_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\obs_line_route_27042020.csv")
put_line_summary_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\put_line_summary_unwanted_lines_removed_27042020.csv")  # change made on 24042020

# initial guess model
ig_stops_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\initial_guess\\ig_stops_mhw_001_17052020.csv")
ig_line_route_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\initial_guess\\ig_line_route_mhw_001_17052020.csv")

# visum defaults
vd_stops_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\visum_default\\visum_default_stops_18052020.csv")
vd_line_route_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\visum_default\\visum_default_line_route_18052020.csv")

# final calibrated model
cal_stops_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_13_1\\calibrated_stops_mhw_001_17052020.csv")
cal_line_route_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_13_1\\calibrated_line_routes_mhw_001_17052020.csv")

cal_stops_sim_improved_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_15\\run_15_simulated_results\\mean_headway\\run_15_mean_headway_001_stops_movements_12072020.csv")
cal_line_route_sim_improved_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_15\\run_15_simulated_results\\mean_headway\\run_15_mean_headway_001_line_routes_12072020.csv")
# keeping important columns
stops_col = ['NO', 'PASSTHROUGHSTOP(AP)', 'PASSTHROUGHNOSTOP(AP)', 'PASSTRANSDIR(AP)', 'PASSTRANSWALKBOARD(AP)',
             'PASSTRANSALIGHTWALK(AP)', 'PASSTRANSTOTAL(AP)']
line_route_col = ['LINENAME', 'NAME', 'DIRECTIONCODE', 'PTRIPSUNLINKED(AP)', 'PTRIPSUNLINKED0(AP)',
                  'PTRIPSUNLINKED1(AP)', 'PTRIPSUNLINKED2(AP)', 'PTRIPSUNLINKED>2(AP)']

change_col_stops_obs = {'PASSTHROUGHSTOP(AP)': 'PASSTHROUGHSTOP(AP)_OBS',
                        'PASSTHROUGHNOSTOP(AP)': 'PASSTHROUGHNOSTOP(AP)_OBS',
                        'PASSTRANSDIR(AP)': 'PASSTRANSDIR(AP)_OBS',
                        'PASSTRANSWALKBOARD(AP)': 'PASSTRANSWALKBOARD(AP)_OBS',
                        'PASSTRANSALIGHTWALK(AP)': 'PASSTRANSALIGHTWALK(AP)_OBS',
                        'PASSTRANSTOTAL(AP)': 'PASSTRANSTOTAL(AP)_OBS'}

change_col_stops_sim = {'PASSTHROUGHSTOP(AP)': 'PASSTHROUGHSTOP(AP)_SIM',
                        'PASSTHROUGHNOSTOP(AP)': 'PASSTHROUGHNOSTOP(AP)_SIM',
                        'PASSTRANSDIR(AP)': 'PASSTRANSDIR(AP)_SIM',
                        'PASSTRANSWALKBOARD(AP)': 'PASSTRANSWALKBOARD(AP)_SIM',
                        'PASSTRANSALIGHTWALK(AP)': 'PASSTRANSALIGHTWALK(AP)_SIM',
                        'PASSTRANSTOTAL(AP)': 'PASSTRANSTOTAL(AP)_SIM'}

change_col_line_route_obs = {'PTRIPSUNLINKED(AP)': 'PTRIPSUNLINKED(AP)_OBS',
                             'PTRIPSUNLINKED0(AP)': 'PTRIPSUNLINKED0(AP)_OBS',
                             'PTRIPSUNLINKED1(AP)': 'PTRIPSUNLINKED1(AP)_OBS',
                             'PTRIPSUNLINKED2(AP)': 'PTRIPSUNLINKED2(AP)_OBS',
                             'PTRIPSUNLINKED>2(AP)': 'PTRIPSUNLINKED>2(AP)_OBS'}

change_col_line_route_sim = {'PTRIPSUNLINKED(AP)': 'PTRIPSUNLINKED(AP)_SIM',
                             'PTRIPSUNLINKED0(AP)': 'PTRIPSUNLINKED0(AP)_SIM',
                             'PTRIPSUNLINKED1(AP)': 'PTRIPSUNLINKED1(AP)_SIM',
                             'PTRIPSUNLINKED2(AP)': 'PTRIPSUNLINKED2(AP)_SIM',
                             'PTRIPSUNLINKED>2(AP)': 'PTRIPSUNLINKED>2(AP)_SIM'}

# selecting important columns
stops_obs_df = stops_obs_df[stops_col]
line_route_obs_df = line_route_obs_df[line_route_col]

ig_stops_sim_df = ig_stops_sim_df[stops_col]
ig_line_route_sim_df = ig_line_route_sim_df[line_route_col]

vd_stops_sim_df = vd_stops_sim_df[stops_col]
vd_line_route_df = vd_line_route_df[line_route_col]

cal_stops_sim_df = cal_stops_sim_df[stops_col]
cal_line_route_sim_df = cal_line_route_sim_df[line_route_col]

# renaming the columns - observed data
stops_obs_df = stops_obs_df.rename(columns=change_col_stops_obs)
line_route_obs_df = line_route_obs_df.rename(columns=change_col_line_route_obs)

# renaming the columns - simulated data
# initial guess
ig_stops_sim_df = ig_stops_sim_df.rename(columns=change_col_stops_sim)
ig_line_route_sim_df = ig_line_route_sim_df.rename(columns=change_col_line_route_sim)

# visum defaults model
vd_stops_sim_df = vd_stops_sim_df.rename(columns=change_col_stops_sim)
vd_line_route_df = vd_line_route_df.rename(columns=change_col_line_route_sim)

# calibrated model - Thesis
cal_stops_sim_df = cal_stops_sim_df.rename(columns=change_col_stops_sim)
cal_line_route_sim_df = cal_line_route_sim_df.rename(columns=change_col_line_route_sim)

# calibrated model - improvements
cal_stops_sim_improved_df = cal_stops_sim_improved_df.rename(columns=change_col_stops_sim)
cal_line_route_sim_improved_df = cal_line_route_sim_improved_df.rename(columns=change_col_line_route_sim)

# merging the data frames
# 1. Merge observed data with simulated  - initial guess
ig_stops_merged_df = stops_obs_df.merge(ig_stops_sim_df, on="NO")
ig_line_routes_merged_df = line_route_obs_df.merge(ig_line_route_sim_df, on=['LINENAME', 'NAME'])

# 2. Merge observed data with simulated - visum default
vd_stops_merged_df = stops_obs_df.merge(vd_stops_sim_df, on='NO')
vd_line_routes_merged_df = line_route_obs_df.merge(vd_line_route_df, on=['LINENAME', 'NAME'])

# 3. Merge observed data with simulated  - calibrated model
cal_stops_merged_df = stops_obs_df.merge(cal_stops_sim_df, on="NO")
cal_line_routes_merged_df = line_route_obs_df.merge(cal_line_route_sim_df, on=['LINENAME', 'NAME'])

# 4. Merge observed data with simulated  - improved model - 13072020
cal_stops_improved_merged_df = stops_obs_df.merge(cal_stops_sim_improved_df, on="NO")
cal_line_routes_improved_merged_df = line_route_obs_df.merge(cal_line_route_sim_improved_df, on=['LINENAME', 'NAME'])

# removing unwanted lines
ig_line_routes_cleaned_df = pd.merge(ig_line_routes_merged_df, put_line_summary_df, left_on='LINENAME',
                                     right_on="PuTLine")
ig_line_routes_cleaned_df = ig_line_routes_cleaned_df[ig_line_routes_cleaned_df['RemoveLine'] == 'keep']

vd_line_routes_cleaned_df = pd.merge(vd_line_routes_merged_df, put_line_summary_df, left_on='LINENAME',
                                     right_on="PuTLine")
vd_line_routes_cleaned_df = vd_line_routes_cleaned_df[vd_line_routes_cleaned_df['RemoveLine'] == 'keep']

cal_line_routes_cleaned_df = pd.merge(cal_line_routes_merged_df, put_line_summary_df, left_on='LINENAME',
                                      right_on="PuTLine")
cal_line_routes_cleaned_df = cal_line_routes_cleaned_df[cal_line_routes_cleaned_df['RemoveLine'] == 'keep']

cal_line_routes_improved_cleaned_df = pd.merge(cal_line_routes_improved_merged_df, put_line_summary_df, left_on='LINENAME',
                                      right_on="PuTLine")
cal_line_routes_improved_cleaned_df = cal_line_routes_improved_cleaned_df[cal_line_routes_improved_cleaned_df['RemoveLine'] == 'keep']

# creating dataframes based on transit modes
ig_bus_df = ig_line_routes_cleaned_df[ig_line_routes_cleaned_df['Mode'] == 'Bus']
ig_lrt_df = ig_line_routes_cleaned_df[ig_line_routes_cleaned_df['Mode'] == 'LRT']
ig_mrt_df = ig_line_routes_cleaned_df[ig_line_routes_cleaned_df['Mode'] == 'MRT']
ig_rail_df = ig_line_routes_cleaned_df[(ig_line_routes_cleaned_df['Mode']=='LRT')|(ig_line_routes_cleaned_df['Mode']=='MRT')]

vd_bus_df = vd_line_routes_cleaned_df[vd_line_routes_cleaned_df['Mode'] == 'Bus']
vd_lrt_df = vd_line_routes_cleaned_df[vd_line_routes_cleaned_df['Mode'] == 'LRT']
vd_mrt_df = vd_line_routes_cleaned_df[vd_line_routes_cleaned_df['Mode'] == 'MRT']
vd_rail_df = vd_line_routes_cleaned_df[(vd_line_routes_cleaned_df['Mode']=='LRT')|(vd_line_routes_cleaned_df['Mode']=='MRT')]

cal_bus_df = cal_line_routes_cleaned_df[cal_line_routes_cleaned_df['Mode'] == 'Bus']
cal_lrt_df = cal_line_routes_cleaned_df[cal_line_routes_cleaned_df['Mode'] == 'LRT']
cal_mrt_df = cal_line_routes_cleaned_df[cal_line_routes_cleaned_df['Mode'] == 'MRT']
cal_rail_df = cal_line_routes_cleaned_df[(cal_line_routes_cleaned_df['Mode']=='LRT')|(cal_line_routes_cleaned_df['Mode']=='MRT')]

cal_bus_improved_df = cal_line_routes_improved_cleaned_df[cal_line_routes_improved_cleaned_df['Mode'] == 'Bus']
cal_lrt_improved_df = cal_line_routes_improved_cleaned_df[cal_line_routes_improved_cleaned_df['Mode'] == 'LRT']
cal_mrt_improved_df = cal_line_routes_improved_cleaned_df[cal_line_routes_improved_cleaned_df['Mode'] == 'MRT']
cal_rail_improved_df = cal_line_routes_improved_cleaned_df[(cal_line_routes_improved_cleaned_df['Mode']=='LRT')|(cal_line_routes_improved_cleaned_df['Mode']=='MRT')]

#cal_mrt_df.to_csv("C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\plots_with_custom_grid lines\\scatter\\cal_test.csv")

#save paths
save_path_modewise = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\plots_with_custom_grid lines\\scatter\\test_13072020.svg"
save_path_transfer_type = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\plots_with_custom_grid lines\\scatter\\test_transfer_type_13072020.svg"

# scatter plot to compare passenger boardings on transport modes
fig1, axs1 = plt.subplots(nrows=3, ncols=3, constrained_layout=True)
(ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9) = axs1
formatter1 = FuncFormatter(thousands)

scatter_plot_axis(ax1, ig_bus_df['PTRIPSUNLINKED(AP)_OBS'], ig_bus_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_vd)
ax1.set_title("(a.1) Pax. boardings - Bus line routes", fontsize=subplot_title_size)
scatter_plot_axis(ax2, cal_bus_df['PTRIPSUNLINKED(AP)_OBS'], cal_bus_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_ig)
ax2.set_title("(a.2) Pax. boardings - Bus line routes", fontsize=subplot_title_size)
scatter_plot_axis(ax3, cal_bus_improved_df['PTRIPSUNLINKED(AP)_OBS'], cal_bus_improved_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_cal)
ax3.set_title("(a.3) Pax. boardings - Bus line routes", fontsize=subplot_title_size)

scatter_plot_axis(ax4, ig_rail_df['PTRIPSUNLINKED(AP)_OBS'], ig_rail_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_vd)
ax4.set_title("(b.1) Pax. boardings - LRT & MRT line routes", fontsize=subplot_title_size)
scatter_plot_axis(ax5, cal_rail_df['PTRIPSUNLINKED(AP)_OBS'], cal_rail_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_ig)
ax5.set_title("(b.2) Pax. boardings - LRT & MRT line routes", fontsize=subplot_title_size)
scatter_plot_axis(ax6, cal_rail_improved_df['PTRIPSUNLINKED(AP)_OBS'], cal_rail_improved_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_cal)
ax6.set_title("(b.3) Pax. boardings - LRT & MRT line routes", fontsize=subplot_title_size)

scatter_plot_axis(ax7, ig_stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], ig_stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], color=scatter_color_vd)
ax7.set_title("(c.1) Pax. transfers - Total", fontsize=subplot_title_size)
scatter_plot_axis(ax8, cal_stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], cal_stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], color=scatter_color_ig)
ax8.set_title("(c.2) Pax. transfers - Total", fontsize=subplot_title_size)
scatter_plot_axis(ax9, cal_stops_improved_merged_df['PASSTRANSTOTAL(AP)_OBS'], cal_stops_improved_merged_df['PASSTRANSTOTAL(AP)_SIM'], color=scatter_color_cal)
ax9.set_title("(c.3) Pax. transfers - Total", fontsize=subplot_title_size)

# scatter_plot_axis(ax7, vd_mrt_df['PTRIPSUNLINKED(AP)_OBS'], vd_mrt_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_vd)
# scatter_plot_axis(ax8, ig_mrt_df['PTRIPSUNLINKED(AP)_OBS'], ig_mrt_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_ig)
# scatter_plot_axis(ax9, cal_mrt_df['PTRIPSUNLINKED(AP)_OBS'], cal_mrt_df['PTRIPSUNLINKED(AP)_SIM'], color=scatter_color_cal)

for ax in axs1.flat:
    # ax.set(xlabel='Observed ($10^3$)', ylabel = 'Simulated ($10^3$)')
    ax.set_xlabel('Observed ($10^3$) (x)', fontsize=6)
    ax.set_ylabel('Simulated ($10^3$) (y)', fontsize=6)
    ax.yaxis.set_major_formatter(formatter1)
    ax.xaxis.set_major_formatter(formatter1)

fig1.savefig(save_path_modewise)

# scatter plot to compare passenger boardings on transport modes
fig2, axs2 = plt.subplots(nrows=3, ncols=3, constrained_layout=True)
(ax10, ax11, ax12), (ax13, ax14, ax15), (ax16, ax17, ax18) = axs2
formatter1 = FuncFormatter(thousands)

scatter_plot_axis(ax10, ig_stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], ig_stops_merged_df['PASSTRANSALIGHTWALK(AP)_SIM'], color=scatter_color_vd)
ax10.set_title("(a.1) Pax. transfers - alight walk", fontsize=subplot_title_size)
scatter_plot_axis(ax11, cal_stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], cal_stops_merged_df['PASSTRANSALIGHTWALK(AP)_SIM'], color=scatter_color_ig)
ax11.set_title("(a.2) Pax. transfers - alight walk", fontsize=subplot_title_size)
scatter_plot_axis(ax12, cal_stops_improved_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], cal_stops_improved_merged_df['PASSTRANSALIGHTWALK(AP)_SIM'], color=scatter_color_cal)
ax12.set_title("(a.3) Pax. transfers - alight walk", fontsize=subplot_title_size)

scatter_plot_axis(ax13, ig_stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], ig_stops_merged_df['PASSTRANSWALKBOARD(AP)_SIM'], color=scatter_color_vd)
ax13.set_title("(b.1) Pax. transfers - walk board", fontsize=subplot_title_size)
scatter_plot_axis(ax14, cal_stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], cal_stops_merged_df['PASSTRANSWALKBOARD(AP)_SIM'], color=scatter_color_ig)
ax14.set_title("(b.2) Pax. transfers - walk board", fontsize=subplot_title_size)
scatter_plot_axis(ax15, cal_stops_improved_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], cal_stops_improved_merged_df['PASSTRANSWALKBOARD(AP)_SIM'], color=scatter_color_cal)
ax15.set_title("(b.3) Pax. transfers - walk board", fontsize=subplot_title_size)

scatter_plot_axis(ax16, ig_stops_merged_df['PASSTRANSDIR(AP)_OBS'], ig_stops_merged_df['PASSTRANSDIR(AP)_SIM'], color=scatter_color_vd)
ax16.set_title("(c.1) Pax. transfers - direct", fontsize=subplot_title_size)
scatter_plot_axis(ax17, cal_stops_merged_df['PASSTRANSDIR(AP)_OBS'], cal_stops_merged_df['PASSTRANSDIR(AP)_SIM'], color=scatter_color_ig)
ax17.set_title("(c.2) Pax. transfers - direct", fontsize=subplot_title_size)
scatter_plot_axis(ax18, cal_stops_improved_merged_df['PASSTRANSDIR(AP)_OBS'], cal_stops_improved_merged_df['PASSTRANSDIR(AP)_SIM'], color=scatter_color_cal)
ax18.set_title("(c.3) Pax. transfers - direct", fontsize=subplot_title_size)

for ax in axs2.flat:
    # ax.set(xlabel='Observed ($10^3$)', ylabel = 'Simulated ($10^3$)')
    ax.set_xlabel('Observed ($10^3$) (x)', fontsize=6)
    ax.set_ylabel('Simulated ($10^3$) (y)', fontsize=6)
    ax.yaxis.set_major_formatter(formatter1)
    ax.xaxis.set_major_formatter(formatter1)

fig2.savefig(save_path_transfer_type)


save_path_transfer_type = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\plots_with_custom_grid lines\\scatter\\test_transfer_flow_mode_13072020.svg"

# scatter plot passenger boardings with transfers across rail and bus
fig3, axs3 = plt.subplots(nrows=4, ncols=2, constrained_layout=True)
(ax19, ax20), (ax21, ax22), (ax23, ax24), (ax25, ax26) = axs3
#(ax19, ax20), (ax21, ax22), (ax23, ax24) = axs3
formatter1 = FuncFormatter(thousands)


#cal_bus_df.to_csv("C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\plots_with_custom_grid lines\\scatter\\cal_bus_df.csv")

scatter_plot_axis_2(ax19, cal_bus_improved_df['PTRIPSUNLINKED0(AP)_OBS'], cal_bus_improved_df['PTRIPSUNLINKED0(AP)_SIM'], color=scatter_color_cal)
ax19.set_title("(a.1) Pax. trips : 0 transfers - Bus", fontsize=subplot_title_size)
scatter_plot_axis_2(ax20, cal_rail_improved_df['PTRIPSUNLINKED0(AP)_OBS'], cal_rail_improved_df['PTRIPSUNLINKED0(AP)_SIM'], color=scatter_color_cal)
ax20.set_title("(a.2) Pax. trips : 0 transfers - LRT & MRT", fontsize=subplot_title_size)

scatter_plot_axis_2(ax21, cal_bus_improved_df['PTRIPSUNLINKED1(AP)_OBS'], cal_bus_improved_df['PTRIPSUNLINKED1(AP)_SIM'], color=scatter_color_cal)
ax21.set_title("(b.1) Pax. trips : 1 transfer - Bus", fontsize=subplot_title_size)
scatter_plot_axis_2(ax22, cal_rail_improved_df['PTRIPSUNLINKED1(AP)_OBS'], cal_rail_improved_df['PTRIPSUNLINKED1(AP)_SIM'], color=scatter_color_cal)
ax22.set_title("(b.2) Pax. trips : 1 transfer - LRT & MRT", fontsize=subplot_title_size)

scatter_plot_axis_2(ax23, cal_bus_improved_df['PTRIPSUNLINKED2(AP)_OBS'], cal_bus_improved_df['PTRIPSUNLINKED2(AP)_SIM'], color=scatter_color_cal)
ax23.set_title("(c.1) Pax. trips : 2 transfers - Bus", fontsize=subplot_title_size)
scatter_plot_axis_2(ax24, cal_rail_improved_df['PTRIPSUNLINKED2(AP)_OBS'], cal_rail_improved_df['PTRIPSUNLINKED2(AP)_SIM'], color=scatter_color_cal)
ax24.set_title("(c.2) Pax. trips : 2 transfers - LRT & MRT", fontsize=subplot_title_size)

scatter_plot_axis_2(ax25, cal_bus_improved_df['PTRIPSUNLINKED>2(AP)_OBS'], cal_bus_improved_df['PTRIPSUNLINKED>2(AP)_SIM'], color=scatter_color_cal)
ax25.set_title("(d.1) Pax. trips : > 2 transfers - Bus", fontsize=subplot_title_size)
scatter_plot_axis_2(ax26, cal_rail_improved_df['PTRIPSUNLINKED>2(AP)_OBS'], cal_rail_improved_df['PTRIPSUNLINKED>2(AP)_SIM'], color=scatter_color_cal)
ax26.set_title("(d.2) Pax. trips : > 2 transfers - LRT & MRT", fontsize=subplot_title_size)

for ax in axs3.flat:
    # ax.set(xlabel='Observed ($10^3$)', ylabel = 'Simulated ($10^3$)')
    ax.set_xlabel('Observed ($10^3$) (x)', fontsize=6)
    ax.set_ylabel('Simulated ($10^3$) (y)', fontsize=6)
    ax.yaxis.set_major_formatter(formatter1)
    ax.xaxis.set_major_formatter(formatter1)

fig3.savefig(save_path_transfer_type)



