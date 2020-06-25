"""
Created to see the difference between two objective function selection methods 1. alternative objective,2.Sum of RMSN
The error terms were normalized for the better comparison
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-white')  # seaborn-white, ggplot

save_path = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\test_colors.svg"

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
plt.rc('figure', figsize=(11.69, 8.27))  # 11.69, 8.27
plt.rc('legend', loc='best')
subplot_title_size = 8

# line styles
line_width = 1.0
plot_threshold = 0.05
y_min = 0
a_color = 'royalblue'  # 'steelblue' #'royalblue' #'dodgerblue'
s_color = 'seagreen'
red='orangered'
purple='darkorchid'
green='forestgreen'
blue= 'royalblue'
ash= 'dimgray'
alpha=0.8

fig1, axs1 = plt.subplots(nrows=2, ncols=2)
(ax1, ax2), (ax3, ax4) = axs1

ax1.plot(s_pax_trips_unlinked0, label='unlinked', color=red, linewidth=line_width, linestyle='-')

ax1.plot(s_pax_trips_unlinked, label='unlinked', color=purple, linewidth=line_width, linestyle=':')
ax1.plot(s_pax_trips_unlinked1, label='unlinked', color=green, linewidth=line_width, linestyle='-.')
ax1.plot(s_pax_trips_unlinked2, label='unlinked', color=blue, linewidth=line_width, linestyle='--')
ax1.plot(s_pax_trips_unlinked_g2, label='unlinked', color=ash, linewidth=line_width, dashes=[3,1])
ax1.legend()
ax1.set_title('abcd', fontsize=subplot_title_size)

ax2.plot(a_pax_trips_unlinked0, alpha=alpha,label='unlinked', color=a_color, linewidth=line_width, linestyle='-')

ax2.plot(a_pax_trips_unlinked, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle=':')
ax2.plot(a_pax_trips_unlinked1, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle='-.')
ax2.plot(a_pax_trips_unlinked2, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle='--')
ax2.plot(a_pax_trips_unlinked_g2, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, dashes=[3,1])
ax2.legend()
ax2.set_title('abcd', fontsize=subplot_title_size)

ax3.plot(s_pax_trans_combined, alpha=alpha, label='unlinked', color=s_color, linewidth=line_width, linestyle='-')

ax3.plot(s_pax_trans_dir, alpha=alpha, label='unlinked', color=s_color, linewidth=line_width, linestyle=':')
ax3.plot(s_pax_trans_alightw, alpha=alpha, label='unlinked', color=s_color, linewidth=line_width, linestyle='-.')
ax3.plot(s_pax_trans_walkb, alpha=alpha, label='unlinked', color=s_color, linewidth=line_width, linestyle='--')
ax3.plot(s_pax_trans_total, alpha=alpha, label='unlinked', color=s_color, linewidth=line_width, dashes=[3,1])
ax3.legend()
ax3.set_title('abcd', fontsize=subplot_title_size)

ax4.plot(a_pax_trans_combined, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle='-')

ax4.plot(a_pax_trans_dir, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle=':')
ax4.plot(a_pax_trans_alightw, alpha=alpha, label='unlinked', color=a_color,linewidth=line_width, linestyle='-.')
ax4.plot(a_pax_trans_walkb, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle='--')
ax4.plot(a_pax_trans_total, alpha=alpha, label='unlinked', color=a_color, linewidth=line_width, linestyle='-')
ax4.legend()
ax4.set_title('abcd', fontsize=subplot_title_size)

# fig1.legend([s1,s2,s3,s4,s5])
# plt.subplots_adjust(right=0.85)
for ax in axs1.flat:
    # ax.set(xlabel='Observed ($10^3$)', ylabel = 'Simulated ($10^3$)')
    ax.set_xlabel('Iteration', fontsize=6)
    ax.set_ylabel('RMSN', fontsize=6)

plt.savefig(save_path)
