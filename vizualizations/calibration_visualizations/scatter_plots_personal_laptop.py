'''
Created on 4 Mar 2020

@author: thenuwan.jayasinghe
@note: To create scatter plots for observed values and calibrated values
'''
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
from matplotlib.ticker import FuncFormatter
import numpy as np

# plot constant
subplot_title_size = 8
scatter_size = 15
scatter_color = 'darkorange'

#arange_increment size

# plots relted custom functions
"""
inspired from https://matplotlib.org/examples/pylab_examples/custom_ticker1.html
"""
def thousands(x, pos):
    'The two args are the value and tick position'
    return '%1.0f' % (x * 1e-3)


# observed data : permenant links
stops_obs_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\obs_stops_04032020.csv")
line_route_obs_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\obs_line_route_27042020.csv")
put_line_summary_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\put_line_summary_unwanted_lines_removed_27042020.csv") #change made on 24042020

# calibration data : link needs to be updated

stops_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_9\\mean_headway_0.01\\run_9_stopsmhw_001.csv")
line_route_sim_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_9\\mean_headway_0.01\\run9_lineroute_mhw_001.csv")

#save results
savepath1 = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\plots\\run_9_stops_mwt001_27042020_1.svg"
savepath2 = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\plots\\run_9_trips_by_mode_mwt001_27042020_1.svg"
savepath3 = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\plots\\run_9_line_route_mwt001_27042020_1.svg"

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

stops_sim_df = stops_sim_df[stops_col]
line_route_sim_df = line_route_sim_df[line_route_col]

# renaming the columns
stops_obs_df = stops_obs_df.rename(columns=change_col_stops_obs)
line_route_obs_df = line_route_obs_df.rename(columns=change_col_line_route_obs)
stops_sim_df = stops_sim_df.rename(columns=change_col_stops_sim)
line_route_sim_df = line_route_sim_df.rename(columns=change_col_line_route_sim)

# merging the data frames
# 1. Merge observed stops with simulated stops

stops_merged_df = stops_obs_df.merge(stops_sim_df, on="NO")
line_routes_merged_df = line_route_obs_df.merge(line_route_sim_df, on=['LINENAME', 'NAME'])

# removing unwanted lines
line_routes_cleaned_df = pd.merge(line_routes_merged_df, put_line_summary_df, left_on='LINENAME', right_on="PuTLine")
# line_routes_cleaned_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\line_cleaned.csv")

# remove lines with no observed values / no time tables
line_routes_cleaned_df = line_routes_cleaned_df[line_routes_cleaned_df['RemoveLine'] == 'keep']

bus_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode'] == 'Bus']
premium_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode'] == 'Premium']
bus_premium_df = line_routes_cleaned_df[
    (line_routes_cleaned_df['Mode'] == 'Bus') | (line_routes_cleaned_df['Mode'] == 'Premium')]

lrt_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode'] == 'LRT']
mrt_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode'] == 'MRT']
lrt_mrt_df = line_routes_cleaned_df[
    (line_routes_cleaned_df['Mode'] == 'LRT') | (line_routes_cleaned_df['Mode'] == 'MRT')]

# stops_merged_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\merged_stops.csv")
# line_routes_merged_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\merged_lines.csv")


#===============================================================================
# plt.scatter(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'])
# b, m = polyfit(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], 1)
# print m
# plt.plot(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_OBS']*m +b)
# plt.plot(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_OBS'])
# plt.show()
#===============================================================================


# ===============================================================================
# plt.scatter(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'])
# b, m = polyfit(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'], 1)
# print m
# plt.plot(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_OBS']*m +b)
# plt.plot(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'])
# plt.show()
# ===============================================================================
plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

fig1, axs1 = plt.subplots(nrows=2, ncols=3, constrained_layout=True)
(ax1, ax2, ax3), (ax4, ax5, ax6) = axs1
formatter1 = FuncFormatter(thousands)

fig1.suptitle("Passenger transfers at stops")
ax1.scatter(stops_merged_df['PASSTRANSDIR(AP)_OBS'], stops_merged_df['PASSTRANSDIR(AP)_SIM'], alpha=0.7, color= scatter_color,
            edgecolors='none', s=scatter_size)
ax1.axis('equal')
ax1_max = max(max(stops_merged_df['PASSTRANSDIR(AP)_OBS']),  max(stops_merged_df['PASSTRANSDIR(AP)_SIM']))
ax1.set(xlim=(0, ax1_max), ylim=(0, ax1_max))
print ax1_max
ax1_max_list = list(np.arange(0, ax1_max, int(ax1_max/20)))
ax1.plot(ax1_max_list, ax1_max_list, linestyle=':',
         color='dimgray', alpha=0.7)
ax1.set_title('PassTransDir', fontsize=subplot_title_size)
b1, m1 = polyfit(stops_merged_df['PASSTRANSDIR(AP)_OBS'], stops_merged_df['PASSTRANSDIR(AP)_SIM'], 1)
ax1.plot(ax1_max_list, pd.Series(ax1_max_list)*m1 +b1, linestyle=':',
         color = 'k', alpha = 0.6)
ax1.text(ax1_max*0.1,ax1_max*0.6,"y = " + str(round(m1,2)) + "x + " + str(round(b1,2)), fontsize=6)


ax2.scatter(stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], stops_merged_df['PASSTRANSWALKBOARD(AP)_SIM'], alpha=0.7,
            color=scatter_color, edgecolors='none', s=scatter_size)
ax2.axis('equal')
ax2_max = max(max(stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS']),max(stops_merged_df['PASSTRANSWALKBOARD(AP)_SIM']))
ax2_max_list = list(np.arange(0, ax2_max, int(ax2_max/20)))
ax2.plot(ax2_max_list, ax2_max_list, linestyle=':',
         color='dimgray', alpha=0.7)
ax2.set_title('PassTransWalkBoard', fontsize=subplot_title_size)
b2, m2 = polyfit(stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], stops_merged_df['PASSTRANSWALKBOARD(AP)_SIM'], 1)
ax2.plot(ax2_max_list, pd.Series(ax2_max_list)*m2 +b2, linestyle=':',
         color = 'k', alpha = 0.6)
ax2.text(ax2_max*0.1,ax2_max*0.6,
         "y = " + str(round(m2,2)) + "x + " + str(round(b2,2)), fontsize=6)


ax3.scatter(stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], stops_merged_df['PASSTRANSALIGHTWALK(AP)_SIM'], alpha=0.7,
            color=scatter_color, edgecolors='none', s=scatter_size)
ax3.axis('equal')
ax3_max = max(max(stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS']) , max(stops_merged_df['PASSTRANSALIGHTWALK(AP)_SIM']))
ax3_max_list = list(np.arange(0, ax3_max, int(ax3_max/20)))
ax3.plot(ax3_max_list, ax3_max_list, linestyle=':',
         color='dimgray', alpha=0.7)
ax3.set_title('PassTransAlightWalk', fontsize=subplot_title_size)
b3, m3 = polyfit(stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], stops_merged_df['PASSTRANSALIGHTWALK(AP)_SIM'], 1)
ax3.plot(ax3_max_list, pd.Series(ax3_max_list)*m3 +b3, linestyle=':',
         color = 'k', alpha = 0.6)
ax3.text(ax3_max*0.1, ax3_max*0.6,
         "y = " + str(round(m3,2)) + "x + " + str(round(b3,2)), fontsize=6)


ax4.scatter(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], alpha=0.7,
            color=scatter_color, edgecolors='none', s=scatter_size)
ax4.axis('equal')
ax4_max = max(max(stops_merged_df['PASSTRANSTOTAL(AP)_OBS']) , max(stops_merged_df['PASSTRANSTOTAL(AP)_SIM']))
ax4_max_list = list(np.arange(0, ax4_max, int(ax4_max/20)))
ax4.plot(ax4_max_list, ax4_max_list, linestyle=':',
         color='dimgray', alpha=0.7)
ax4.set_title('PassTransTotal', fontsize=subplot_title_size)
b4, m4 = polyfit(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], 1)
ax4.plot(ax4_max_list, pd.Series(ax4_max_list)*m4 + b4, linestyle=':',
         color = 'k', alpha = 0.6)
ax4.text(ax4_max*0.1, ax4_max*0.6,
         "y = " + str(round(m4,2)) + "x + " + str(round(b4,2)), fontsize=6)


ax5.scatter(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'], alpha=0.7,
            color=scatter_color, edgecolors='none', s=scatter_size)
ax5.axis('equal')
ax5_max = max(max(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS']) , max(stops_merged_df['PASSTHROUGHSTOP(AP)_SIM']))
ax5_max_list = list(np.arange(0, ax5_max, int(ax5_max/20)))
ax5.plot(ax5_max_list, ax5_max_list, linestyle=':',
         color='dimgray', alpha=0.7)
ax5.set_title('PassThroughStop', fontsize=subplot_title_size)
b5, m5 = polyfit(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'], 1)
ax5.plot(ax5_max_list, pd.Series(ax5_max_list)*m5 +b5, linestyle=':',
         color = 'k', alpha = 0.6)
ax5.text(ax5_max*0.1, ax5_max*0.6,
         "y = " + str(round(m5,2)) + "x + "+ str(round(b5,2)), fontsize=6)



ax6.scatter(stops_merged_df['PASSTHROUGHNOSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHNOSTOP(AP)_SIM'], alpha=0.7,
            color=scatter_color, edgecolors='none', s=scatter_size)
ax6.axis('equal')
ax6_max = max(max(stops_merged_df['PASSTHROUGHNOSTOP(AP)_OBS']), max(stops_merged_df['PASSTHROUGHNOSTOP(AP)_SIM']))
ax6_max_list = list(np.arange(0, ax6_max, int(ax6_max/20)))
ax6.plot(ax6_max_list, ax6_max_list, linestyle=':',
         color='dimgray', alpha=0.7)
ax6.set_title('PassThroughNoStop', fontsize=subplot_title_size)
b6, m6 = polyfit(stops_merged_df['PASSTHROUGHNOSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHNOSTOP(AP)_SIM'], 1)
ax6.plot(ax6_max_list, pd.Series(ax6_max_list)*m6 +b6, linestyle=':',
         color = 'k', alpha = 0.6)
ax6.text(ax6_max*0.1, ax6_max*0.6,
         "y = " + str(round(m6,2)) + "x + " + str(round(b6,2)), fontsize=6)


for ax in axs1.flat:
    # ax.set(xlabel='Observed ($10^3$)', ylabel = 'Simulated ($10^3$)')
    ax.set_xlabel('Observed ($10^3$)', fontsize=6)
    ax.set_ylabel('Simulated ($10^3$)', fontsize=6)
    ax.yaxis.set_major_formatter(formatter1)
    ax.xaxis.set_major_formatter(formatter1)


fig1.savefig(savepath1)

# passenger transfer plot
fig2, axs2 = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
(ax7, ax8), (ax9, ax10) = axs2
formatter3 = FuncFormatter(thousands)

ax7.scatter(line_routes_cleaned_df['PTRIPSUNLINKED(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED(AP)_SIM'],
            alpha=0.7, color=scatter_color, edgecolors='none')
ax7.axis('equal')
ax7_max = max(max(line_routes_cleaned_df['PTRIPSUNLINKED(AP)_OBS']) , max(line_routes_cleaned_df['PTRIPSUNLINKED(AP)_SIM']))
ax7_max_list = list(np.arange(0, ax7_max, int(ax7_max/20)))
ax7.plot(ax7_max_list, ax7_max_list,
         linestyle=':', color='dimgray', alpha=0.7)
ax7.set_title('PTripsUnlinked')
b7, m7 = polyfit(line_routes_cleaned_df['PTRIPSUNLINKED(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED(AP)_SIM'], 1)
ax7.plot(ax7_max_list, pd.Series(ax7_max_list)*m7 +b7, linestyle=':',
         color = 'k', alpha = 0.6)
ax7.text(ax7_max*0.1, ax7_max*0.6,
         "y = " + str(round(m7,2)) + "x + " + str(round(b7,2)), fontsize=6)


ax8.scatter(line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_SIM'],
            alpha=0.7, color=scatter_color, edgecolors='none')
ax8.axis('equal')
ax8_max = max(max(line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_OBS']) , max(line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_SIM']))
ax8_max_list = list(np.arange(0, ax8_max, int(ax8_max/20)))
ax8.plot(ax8_max_list, ax8_max_list,
         linestyle=':', color='dimgray', alpha=0.7)
ax8.set_title('PTripsUnlinked - 1 Transfer')
b8, m8 = polyfit(line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_SIM'], 1)
ax8.plot(ax8_max_list, pd.Series(ax8_max_list)*m8 +b8, linestyle=':',
         color = 'k', alpha = 0.6)
ax8.text(ax8_max*0.1, ax8_max*0.6,
         "y = " + str(round(m8,2)) + "x + " + str(round(b8,2)), fontsize=6)


ax9.scatter(line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_SIM'],
            alpha=0.7, color=scatter_color, edgecolors='none')
ax9.axis('equal')
ax9_max = max(max(line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_OBS']) , max(line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_SIM']))
ax9_max_list = list(np.arange(0, ax9_max, int(ax9_max/20)))
ax9.plot(ax9_max_list, ax9_max_list,
         linestyle=':', color='dimgray', alpha=0.7)
ax9.set_title('PTripsUnlinked - 2 Transfer')
b9, m9 = polyfit(line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_SIM'], 1)
ax9.plot(ax9_max_list, pd.Series(ax9_max_list)*m9 +b9, linestyle=':',
         color = 'k', alpha = 0.6)
ax9.text(ax9_max*0.1, ax9_max*0.6,
         "y = " + str(round(m9,2)) + "x + " + str(round(b9,2)), fontsize=6)


ax10.scatter(line_routes_cleaned_df['PTRIPSUNLINKED2(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED2(AP)_SIM'],
             alpha=0.7, color=scatter_color, edgecolors='none')
ax10.axis('equal')
ax10_max = max(max(line_routes_cleaned_df['PTRIPSUNLINKED2(AP)_OBS']) , max(line_routes_cleaned_df['PTRIPSUNLINKED2(AP)_SIM']))
ax10_max_list = list(np.arange(0, ax10_max, int(ax10_max/20)))
ax10.plot(ax10_max_list, ax10_max_list,
          linestyle=':', color='dimgray', alpha=0.7)
ax10.set_title('PTripsUnlinked - 3 Transfer')
b10, m10 = polyfit(line_routes_cleaned_df['PTRIPSUNLINKED2(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED2(AP)_SIM'], 1)
ax10.plot(ax10_max_list, pd.Series(ax10_max_list)*m10 +b10, linestyle=':',
         color = 'k', alpha = 0.6)
ax10.text(ax10_max*0.1, ax10_max*0.6,
         "y = " + str(round(m10,2)) + "x + " + str(round(b10,2)), fontsize=6)


for ax in axs2.flat:
    ax.set_xlabel('Observed ($10^3$)', fontsize=6)
    ax.set_ylabel('Simulated ($10^3$)', fontsize=6)
    ax.yaxis.set_major_formatter(formatter3)
    ax.xaxis.set_major_formatter(formatter3)


fig2.savefig(savepath3)

# mode related  counts
fig3, axs3 = plt.subplots(nrows=2, ncols=3, constrained_layout=True)
(ax11, ax12, ax13), (ax14, ax15, ax16) = axs3
formatter2 = FuncFormatter(thousands)

fig3.suptitle('PuT Lines')

ax11.scatter(bus_df['PTRIPSUNLINKED(AP)_OBS'], bus_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color=scatter_color,
             edgecolors='none', s=scatter_size)
ax11.axis('equal')
ax11_max = max(max(bus_df['PTRIPSUNLINKED(AP)_OBS']), max(bus_df['PTRIPSUNLINKED(AP)_SIM']))
ax11_max_list = list(np.arange(0, ax11_max, int(ax11_max/20)))
ax11.plot(ax11_max_list, ax11_max_list, linestyle=':', color='dimgray', alpha=0.7)
ax11.set_title('Standard Bus Only', fontsize=subplot_title_size)
b11, m11 = polyfit(bus_df['PTRIPSUNLINKED(AP)_OBS'], bus_df['PTRIPSUNLINKED(AP)_SIM'], 1)
ax11.plot(ax11_max_list, pd.Series(ax11_max_list)*m11 +b11, linestyle=':',
         color = 'k', alpha = 0.6)
ax11.text(ax11_max*0.1, ax11_max*0.6,
         "y = " + str(round(m11,2)) + "x + " + str(round(b11,2)), fontsize=6)


# ax12.scatter(premium_df['PTRIPSUNLINKED(AP)_OBS'], premium_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color=scatter_color,
#              edgecolors='none', s=scatter_size)
# ax12_max = max(premium_df['PTRIPSUNLINKED(AP)_OBS'] + premium_df['PTRIPSUNLINKED(AP)_SIM'])
# ax12_max_list = list(np.arange(0, ax12_max, int(ax12_max/20)))
# ax12.plot(ax12_max_list, ax12_max_list, linestyle=':', color='dimgray',
#           alpha=0.7)
# ax12.set_title('Premium Bus Only', fontsize=subplot_title_size)
# b12, m12 = polyfit(premium_df['PTRIPSUNLINKED(AP)_OBS'], premium_df['PTRIPSUNLINKED(AP)_SIM'], 1)
# ax12.plot(ax12_max_list, pd.Series(ax12_max_list)*m12 +b12, linestyle=':',
#          color = 'k', alpha = 0.6)
# ax12.text(ax12_max*0.1, ax12_max*0.6,
#          "y = " + str(round(m12,2)) + "x + " + str(round(b12,2)), fontsize=6)


# ax13.scatter(bus_premium_df['PTRIPSUNLINKED(AP)_OBS'], bus_premium_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7,
#              color=scatter_color, edgecolors='none', s=scatter_size)
# ax13_max = max(bus_premium_df['PTRIPSUNLINKED(AP)_OBS'] + bus_premium_df['PTRIPSUNLINKED(AP)_SIM'])
# ax13_max_list = list(np.arange(0, ax13_max, int(ax13_max/20)))
# ax13.plot(ax13_max_list, ax13_max_list, linestyle=':',
#           color='dimgray', alpha=0.7)
# ax13.set_title('Standard and Premium Bus', fontsize=subplot_title_size)
# b13, m13 = polyfit(bus_premium_df['PTRIPSUNLINKED(AP)_OBS'], bus_premium_df['PTRIPSUNLINKED(AP)_SIM'], 1)
# ax13.plot(ax13_max_list, pd.Series(ax13_max_list)*m13 +b13, linestyle=':',
#          color = 'k', alpha = 0.6)
# ax13.text(ax13_max*0.1, ax13_max*0.6,
#          "y = " + str(round(m13,2)) + "x + " + str(round(b13,2)), fontsize=6)


ax14.scatter(lrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color=scatter_color,
             edgecolors='none', s=scatter_size)
ax14.axis('equal')
ax14_max = max(max(lrt_df['PTRIPSUNLINKED(AP)_OBS']) , max(lrt_df['PTRIPSUNLINKED(AP)_SIM']))
ax14_max_list = list(np.arange(0, ax14_max, int(ax14_max/20)))
ax14.plot(ax14_max_list, ax14_max_list, linestyle=':', color='dimgray', alpha=0.7)
ax14.set_title('LRT only', fontsize=subplot_title_size)
b14, m14 = polyfit(lrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_df['PTRIPSUNLINKED(AP)_SIM'], 1)
ax14.plot(ax14_max_list, pd.Series(ax14_max_list)*m14 +b14, linestyle=':',
         color = 'k', alpha = 0.6)
ax14.text(ax14_max*0.1, ax14_max*0.6,
         "y = " + str(round(m14,2)) + "x + " + str(round(b14,2)), fontsize=6)


ax15.scatter(mrt_df['PTRIPSUNLINKED(AP)_OBS'], mrt_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color=scatter_color,
             edgecolors='none', s=scatter_size)
ax15.axis('equal')
ax15_max = max(max(mrt_df['PTRIPSUNLINKED(AP)_OBS']), max(mrt_df['PTRIPSUNLINKED(AP)_SIM']))
ax15_max_list = list(np.arange(0, ax15_max, int(ax15_max/20)))
ax15.plot(ax15_max_list, ax15_max_list, linestyle=':', color='dimgray', alpha=0.7)
ax15.set_title('MRT only', fontsize=subplot_title_size)
b15, m15 = polyfit(mrt_df['PTRIPSUNLINKED(AP)_OBS'], mrt_df['PTRIPSUNLINKED(AP)_SIM'], 1)
ax15.plot(ax15_max_list, pd.Series(ax15_max_list)*m15 +b15, linestyle=':',
         color = 'k', alpha = 0.6)
ax15.text(ax15_max*0.1, ax15_max*0.6,
         "y = " + str(round(m15,2)) + "x + "+ str(round(b15,2)), fontsize=6)


ax16.scatter(lrt_mrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_mrt_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color=scatter_color,
             edgecolors='none', s=scatter_size)
ax15.axis('equal')
ax16_max = max(max(lrt_mrt_df['PTRIPSUNLINKED(AP)_OBS']), max(lrt_mrt_df['PTRIPSUNLINKED(AP)_SIM']))
ax16_max_list = list(np.arange(0, ax16_max, int(ax16_max/20)))
ax16.plot(ax16_max_list, ax16_max_list, linestyle=':', color='dimgray',
          alpha=0.7)
ax16.set_title('LRT and MRT', fontsize=subplot_title_size)
b16, m16 = polyfit(lrt_mrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_mrt_df['PTRIPSUNLINKED(AP)_SIM'], 1)
ax16.plot(ax16_max_list, pd.Series(ax16_max_list)*m16 +b16, linestyle=':',
         color = 'k', alpha = 0.6)
ax16.text(ax16_max*0.1, ax16_max*0.6,
         "y = " + str(round(m16,2)) + "x + " + str(round(b16,2)), fontsize=6)


for ax in axs3.flat:
    ax.set_xlabel('Observed ($10^3$)', fontsize=6)
    ax.set_ylabel('Simulated ($10^3$)', fontsize=6)
    ax.yaxis.set_major_formatter(formatter1)
    ax.xaxis.set_major_formatter(formatter1)


fig3.savefig(savepath2)
