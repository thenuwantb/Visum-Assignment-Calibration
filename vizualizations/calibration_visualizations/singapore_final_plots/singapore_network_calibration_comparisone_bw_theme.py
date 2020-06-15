"""
Created to see the difference between two objective function selection methods 1. alternative objective,2.Sum of RMSN
The error terms were normalized for the better comparison
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('grayscale')  # seaborn-white, ggplot

save_path = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\grayscale_dot.svg"

sum_objective_norm_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_12\\run_12_results_normalized_09052020.csv")
alternate_objective_norm_df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_13\\run_13_results_normalized_09052020.csv")

a_pax_trans_alightw = alternate_objective_norm_df['pax_trans_alightw_rmsn'].tolist()
a_pax_trans_dir = alternate_objective_norm_df['pass_trans_dir_rmsn'].tolist()
a_pax_trans_walkb = alternate_objective_norm_df['pax_trans_walkb_rmsn'].tolist()
a_pax_trans_total = alternate_objective_norm_df['pax_trans_total_rmsn'].tolist()
a_pax_trans_combined = alternate_objective_norm_df['pass_trans_total_combined_rmsn'].tolist()

a_pax_trips_unlinked = alternate_objective_norm_df['pax_trips_unlinked_rmsn'].tolist()
a_pax_trips_unlinked0 = alternate_objective_norm_df['pax_trips_unlinked_0_rmsn'].tolist()
a_pax_trips_unlinked1 = alternate_objective_norm_df['pax_trips_unlinked_1_rmsn'].tolist()
a_pax_trips_unlinked2 = alternate_objective_norm_df['pax_trips_unlinked_2_rmsn'].tolist()
a_pax_trips_unlinked_g2 = alternate_objective_norm_df['pax_trips_unlinked_g_2_rmsn'].tolist()

s_pax_trans_alightw = sum_objective_norm_df['pax_trans_alightw_rmsn'].tolist()
s_pax_trans_dir = sum_objective_norm_df['pass_trans_dir_rmsn'].tolist()
s_pax_trans_walkb = sum_objective_norm_df['pax_trans_walkb_rmsn'].tolist()
s_pax_trans_total = sum_objective_norm_df['pax_trans_total_rmsn'].tolist()
s_pax_trans_combined = sum_objective_norm_df['pass_trans_total_combined_rmsn'].tolist()

s_pax_trips_unlinked = sum_objective_norm_df['pax_trips_unlinked_rmsn'].tolist()
s_pax_trips_unlinked0 = sum_objective_norm_df['pax_trips_unlinked_0_rmsn'].tolist()
s_pax_trips_unlinked1 = sum_objective_norm_df['pax_trips_unlinked_1_rmsn'].tolist()
s_pax_trips_unlinked2 = sum_objective_norm_df['pax_trips_unlinked_2_rmsn'].tolist()
s_pax_trips_unlinked_g2 = sum_objective_norm_df['pax_trips_unlinked_g_2_rmsn'].tolist()

## Figure
plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('figure', figsize=(11.69, 7.27))  # 11.69, 8.27
# plt.rc('legend', loc='best')

subplot_title_size = 8

# line styles85
line_width = 1.0
plot_threshold = 0.05
y_min = 0
a_color = 'royalblue'  # 'steelblue' #'royalblue' #'dodgerblue'
s_color = 'seagreen'
red = 'orangered'
purple = 'darkorchid'
green = 'forestgreen'
blue = 'royalblue'
ash = 'dimgray'
alpha = 0.7

fig1, axs1 = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
(ax1, ax2), (ax3, ax4) = axs1

ax1.plot(s_pax_trips_unlinked0, alpha=alpha, label='0 transfers ($OF_1$)', linewidth=2.0, linestyle='-')


ax1.plot(s_pax_trips_unlinked1, alpha=alpha, label='1 transfer', linewidth=line_width, linestyle='-.')
ax1.plot(s_pax_trips_unlinked2, alpha=alpha, label='2 transfers', linewidth=line_width, linestyle=':')
ax1.plot(s_pax_trips_unlinked_g2, alpha=alpha, label='> 2 transfers', linewidth=line_width, linestyle='--')
ax1.plot(s_pax_trips_unlinked, alpha=alpha, label='boardings', linewidth=line_width, dashes=[3,1])
ax1.legend(fontsize=8)
ax1.set_title('(a.1) Passenger trips on line routes - SOF', fontsize=subplot_title_size)

ax2.plot(a_pax_trips_unlinked0, alpha=alpha, label='0 transfers ($OF_1$)', linewidth=2.0, linestyle='-')

ax2.plot(a_pax_trips_unlinked1, alpha=alpha, label='1 transfer', linewidth=line_width, linestyle='-.')
ax2.plot(a_pax_trips_unlinked2, alpha=alpha, label='2 transfers', linewidth=line_width, linestyle=':')
ax2.plot(a_pax_trips_unlinked_g2, alpha=alpha, label='> 2 transfers', linewidth=line_width, linestyle='--')
ax2.plot(a_pax_trips_unlinked, alpha=alpha, label='boardings', linewidth=line_width, dashes=[3,1])
ax2.legend(fontsize=8)
ax2.set_title('(a.2) Passenger trips on line routes - DOF', fontsize=subplot_title_size)

ax3.plot(s_pax_trans_combined, alpha=alpha, label='combined ($OF_2$)', linewidth=2.0, linestyle='-')

ax3.plot(s_pax_trans_dir, alpha=alpha, label='direct', linewidth=line_width, linestyle='-.')
ax3.plot(s_pax_trans_alightw, alpha=alpha, label='alight walk', linewidth=line_width, linestyle=':')
ax3.plot(s_pax_trans_walkb, alpha=alpha, label='walk board', linewidth=line_width, linestyle='--')
ax3.plot(s_pax_trans_total, alpha=alpha, label='total', linewidth=line_width, dashes = [3,1])
ax3.legend(fontsize=8)
ax3.set_title('(b.1) Passenger transfers at stops - SOF', fontsize=subplot_title_size)

ax4.plot(a_pax_trans_combined, alpha=alpha, label='combined ($OF_2$)', linewidth=2.0, linestyle='-')

ax4.plot(a_pax_trans_dir, alpha=alpha, label='direct', linewidth=line_width, linestyle='-.')
ax4.plot(a_pax_trans_alightw, alpha=alpha, label='alight walk', linewidth=line_width, linestyle=':')
ax4.plot(a_pax_trans_walkb, alpha=alpha, label='walk board', linewidth=line_width, linestyle='--')
ax4.plot(a_pax_trans_total, alpha=alpha, label='total', linewidth=line_width, dashes = [3,1])
ax4.legend(fontsize=8)
ax4.set_title('(b.2) Passenger transfers at stops - DOF', fontsize=subplot_title_size)

# fig1.legend([s1,s2,s3,s4,s5])
# plt.subplots_adjust(right=0.85)
for ax in axs1.flat:
    # ax.set(xlabel='Observed ($10^3$)', ylabel = 'Simulated ($10^3$)')
    ax.set_xlabel('Iteration', fontsize=6)
    ax.set_ylabel('RMSN', fontsize=6)

plt.savefig(save_path)
