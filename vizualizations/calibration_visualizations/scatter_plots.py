'''
Created on 4 Mar 2020

@author: thenuwan.jayasinghe
@note: To create scatter plots for observed values and calibrated values
'''
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit

# observed data : permenant links
stops_obs_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\obs_stops_04032020.csv")
line_route_obs_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\obs_line_route_04032020.csv")
put_line_summary_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\put_line_summary.csv")

# calibration data : link needs to be updated

stops_sim_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run1\\run_1_stops.csv")
line_route_sim_df = pd.read_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run1\\run_1_line_route.csv")

# keeping important columns
stops_col = ['NO', 'PASSTHROUGHSTOP(AP)', 'PASSTHROUGHNOSTOP(AP)', 'PASSTRANSDIR(AP)', 'PASSTRANSWALKBOARD(AP)', 'PASSTRANSALIGHTWALK(AP)', 'PASSTRANSTOTAL(AP)']
line_route_col = ['LINENAME', 'NAME', 'DIRECTIONCODE', 'PTRIPSUNLINKED(AP)', 'PTRIPSUNLINKED0(AP)', 'PTRIPSUNLINKED1(AP)', 'PTRIPSUNLINKED2(AP)', 'PTRIPSUNLINKED>2(AP)']

change_col_stops_obs = {'PASSTHROUGHSTOP(AP)':'PASSTHROUGHSTOP(AP)_OBS',
                        'PASSTHROUGHNOSTOP(AP)':'PASSTHROUGHNOSTOP(AP)_OBS',
                        'PASSTRANSDIR(AP)':'PASSTRANSDIR(AP)_OBS',
                        'PASSTRANSWALKBOARD(AP)':'PASSTRANSWALKBOARD(AP)_OBS',
                        'PASSTRANSALIGHTWALK(AP)': 'PASSTRANSALIGHTWALK(AP)_OBS',
                        'PASSTRANSTOTAL(AP)':'PASSTRANSTOTAL(AP)_OBS'}

change_col_stops_sim = {'PASSTHROUGHSTOP(AP)':'PASSTHROUGHSTOP(AP)_SIM',
                        'PASSTHROUGHNOSTOP(AP)':'PASSTHROUGHNOSTOP(AP)_SIM',
                        'PASSTRANSDIR(AP)':'PASSTRANSDIR(AP)_SIM',
                        'PASSTRANSWALKBOARD(AP)':'PASSTRANSWALKBOARD(AP)_SIM',
                        'PASSTRANSALIGHTWALK(AP)': 'PASSTRANSALIGHTWALK(AP)_SIM',
                        'PASSTRANSTOTAL(AP)':'PASSTRANSTOTAL(AP)_SIM'}

change_col_line_route_obs = {'PTRIPSUNLINKED(AP)':'PTRIPSUNLINKED(AP)_OBS',
                             'PTRIPSUNLINKED0(AP)':'PTRIPSUNLINKED0(AP)_OBS',
                             'PTRIPSUNLINKED1(AP)':'PTRIPSUNLINKED1(AP)_OBS',
                             'PTRIPSUNLINKED2(AP)':'PTRIPSUNLINKED2(AP)_OBS',
                             'PTRIPSUNLINKED>2(AP)':'PTRIPSUNLINKED>2(AP)_OBS'}

change_col_line_route_sim = {'PTRIPSUNLINKED(AP)':'PTRIPSUNLINKED(AP)_SIM',
                             'PTRIPSUNLINKED0(AP)':'PTRIPSUNLINKED0(AP)_SIM',
                             'PTRIPSUNLINKED1(AP)':'PTRIPSUNLINKED1(AP)_SIM',
                             'PTRIPSUNLINKED2(AP)':'PTRIPSUNLINKED2(AP)_SIM',
                             'PTRIPSUNLINKED>2(AP)':'PTRIPSUNLINKED>2(AP)_SIM'}

# selecting important columns
stops_obs_df = stops_obs_df[stops_col]
line_route_obs_df = line_route_obs_df[line_route_col]

stops_sim_df = stops_sim_df[stops_col]
line_route_sim_df =line_route_sim_df[line_route_col]

# renaming the columns
stops_obs_df = stops_obs_df.rename(columns=change_col_stops_obs)
line_route_obs_df = line_route_obs_df.rename(columns=change_col_line_route_obs)
stops_sim_df = stops_sim_df.rename(columns=change_col_stops_sim)
line_route_sim_df = line_route_sim_df.rename(columns=change_col_line_route_sim)

# merging the data frames
# 1. Merge observed stops with simulated stops

stops_merged_df = stops_obs_df.merge(stops_sim_df, on = "NO")
line_routes_merged_df = line_route_obs_df.merge(line_route_sim_df, on = ['LINENAME', 'NAME'])

#removing unwanted lines
line_routes_cleaned_df = pd.merge(line_routes_merged_df, put_line_summary_df, left_on='LINENAME', right_on = "PuTLine")
#line_routes_cleaned_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\line_cleaned.csv")

# remove lines with no observed values / no time tables
line_routes_cleaned_df = line_routes_cleaned_df[line_routes_cleaned_df['RemoveLine'] == 'keep']

bus_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode']=='Bus']
premium_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode']=='Premium']
bus_premium_df = line_routes_cleaned_df[(line_routes_cleaned_df['Mode'] == 'Bus') | (line_routes_cleaned_df['Mode'] == 'Premium')]
print bus_premium_df.head()

lrt_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode']=='LRT']
mrt_df = line_routes_cleaned_df[line_routes_cleaned_df['Mode']=='MRT']
lrt_mrt_df = line_routes_cleaned_df[(line_routes_cleaned_df['Mode'] == 'LRT') | (line_routes_cleaned_df['Mode'] == 'MRT')]


#stops_merged_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\merged_stops.csv")
#line_routes_merged_df.to_csv("C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\observed_data\\to_plot\\merged_lines.csv")

#===============================================================================
# plt.scatter(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'])
# b, m = polyfit(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], 1)
# print m
# plt.plot(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_OBS']*m +b)
# plt.plot(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_OBS'])
# plt.show()
#===============================================================================

#===============================================================================
# plt.scatter(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'])
# b, m = polyfit(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'], 1)
# print m
# plt.plot(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_OBS']*m +b)
# plt.plot(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'])
# plt.show()
#===============================================================================

fig1,  axs1= plt.subplots(nrows = 2, ncols = 3)
(ax1, ax2, ax3), (ax4, ax5, ax6) = axs1

fig1.suptitle("Passenger transfers at stops")
#ax6.scatter(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'])
ax1.scatter(stops_merged_df['PASSTRANSDIR(AP)_OBS'], stops_merged_df['PASSTRANSDIR(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax1.plot(stops_merged_df['PASSTRANSDIR(AP)_OBS'], stops_merged_df['PASSTRANSDIR(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax1.set_title('PassTransDir')

ax2.scatter(stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], stops_merged_df['PASSTRANSWALKBOARD(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax2.plot(stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], stops_merged_df['PASSTRANSWALKBOARD(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax2.set_title('PassTransWalkBoard')

ax3.scatter(stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], stops_merged_df['PASSTRANSALIGHTWALK(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax3.plot(stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], stops_merged_df['PASSTRANSALIGHTWALK(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax3.set_title('PassTransAlightWalk')

ax4.scatter(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax4.plot(stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], stops_merged_df['PASSTRANSTOTAL(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax4.set_title('PassTransTotal')

ax5.scatter(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax5.plot(stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHSTOP(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax5.set_title('PassThroughStop')

ax6.scatter(stops_merged_df['PASSTHROUGHNOSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHNOSTOP(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax6.plot(stops_merged_df['PASSTHROUGHNOSTOP(AP)_OBS'], stops_merged_df['PASSTHROUGHNOSTOP(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax6.set_title('PassThroughNoStop')

for ax in axs1.flat:
    ax.set(xlabel='Observed', ylabel = 'Simulated') 

plt.savefig()

#===============================================================================
# 
# 
# fig2, axs2 = plt.subplots(nrows = 1, ncols = 3)
# ax7, ax8, ax9 = axs2
# 
# ax7.scatter(line_routes_cleaned_df['PTRIPSUNLINKED(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
# ax7.plot(line_routes_cleaned_df['PTRIPSUNLINKED(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
# ax7.set_title('PTripsUnlinked')
# 
# ax8.scatter(line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
# ax8.plot(line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED0(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
# ax8.set_title('PTripsUnlinked - 1 Transfer')
# 
# ax9.scatter(line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
# ax9.plot(line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_OBS'], line_routes_cleaned_df['PTRIPSUNLINKED1(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
# ax9.set_title('PTripsUnlinked - 2 Transfer')
# 
# plt.show()
#===============================================================================

fig3,  axs3= plt.subplots(nrows = 2, ncols = 3)
(ax10, ax11, ax12), (ax13, ax14, ax15) = axs3

fig3.suptitle('PuT Lines')

ax10.scatter(bus_df['PTRIPSUNLINKED(AP)_OBS'], bus_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax10.plot(bus_df['PTRIPSUNLINKED(AP)_OBS'], bus_df['PTRIPSUNLINKED(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax10.set_title('Standard Bus Only')

ax11.scatter(premium_df['PTRIPSUNLINKED(AP)_OBS'], premium_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax11.plot(premium_df['PTRIPSUNLINKED(AP)_SIM'], premium_df['PTRIPSUNLINKED(AP)_SIM'], linestyle=':', color='dimgray', alpha = 0.7)
ax11.set_title('Premium Bus Only')

ax12.scatter(bus_premium_df['PTRIPSUNLINKED(AP)_OBS'], bus_premium_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax12.plot(bus_premium_df['PTRIPSUNLINKED(AP)_OBS'], bus_premium_df['PTRIPSUNLINKED(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax12.set_title('Standard and Premium Bus')

ax13.scatter(lrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax13.plot(lrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_df['PTRIPSUNLINKED(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax13.set_title('LRT only')

ax14.scatter(mrt_df['PTRIPSUNLINKED(AP)_OBS'], mrt_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax14.plot(mrt_df['PTRIPSUNLINKED(AP)_OBS'], mrt_df['PTRIPSUNLINKED(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax14.set_title('MRT only')

ax15.scatter(lrt_mrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_mrt_df['PTRIPSUNLINKED(AP)_SIM'], alpha=0.7, color = 'teal', edgecolors='none')
ax15.plot(lrt_mrt_df['PTRIPSUNLINKED(AP)_OBS'], lrt_mrt_df['PTRIPSUNLINKED(AP)_OBS'], linestyle=':', color='dimgray', alpha = 0.7)
ax15.set_title('LRT and MRT')

for ax in axs3.flat:
    ax.set(xlabel='Observed', ylabel = 'Simulated') 

plt.show()
