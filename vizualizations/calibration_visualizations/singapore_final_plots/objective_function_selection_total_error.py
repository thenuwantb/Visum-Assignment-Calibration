import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

plt.style.use('seaborn-ticks')

plt.rc('font', family='Arial')
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
plt.rc('figure', figsize=(8.27, 3.5))


def add_gridline(axis):
    axis.grid(linestyle=':', linewidth=0.5, color='darkgray')


red = 'orangered'
purple = 'darkorchid'
green = 'forestgreen'
blue = 'royalblue'

alpha = 0.7
of_1_marker = 'o'
of_2_marker = 's'
mapping = {'one': of_1_marker, 'two': of_2_marker}
marker_face_color = {'one': red, 'two': blue}

df = pd.read_csv(
    "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\run_13\\total_error_change.csv")
norm_rmsn = df['Normalized'].tolist()
objective_function = df['OF'].tolist()
iteration = list(range(0, len(norm_rmsn)))

# custom legend
of_1 = mlines.Line2D([], [], marker=of_1_marker, label='$OF_1$ - direct trips (0 transfers)', mec=red, fillstyle='none', ls='none')
of_2 = mlines.Line2D([], [], marker=of_2_marker, label='$OF_2$ - combined transfers', mec=blue, fillstyle='none', ls='none')
error_line = mpatches.Patch(color='gray', label='Total error', ls='-', lw=0.1)

fig1, ax1 = plt.subplots(nrows=1, ncols=1, constrained_layout=True)

save_path = "C:\\Users\\thenu\\OneDrive - tum.de\\Thesis\\1_Coding\\Experiments\\27022020_singapore_network\\results\\singapore_final_plots\\plots_with_custom_grid lines\\OF_evaluated.svg"

for iter_, norm_ in zip(iteration, norm_rmsn):
    ax1.plot(iter_, norm_, linestyle=':', marker=mapping[objective_function[iter_]],
             mfc=None, mec=marker_face_color[objective_function[iter_]], alpha=0.75, fillstyle='none', markersize=4)
    # ax1.plot(iter_, norm_, linestyle = '-')
ax1.plot(norm_rmsn, color='gray', alpha=0.7)
# ax1.legend(handles=[of_1, of_2, error_line] , fontsize=6)#title='Objective function evaluated'
# ax1.legend().set_title('Objective function evaluated', prop={'size':6})
lg=ax1.legend(handles=[of_1, of_2], title='Objective function evaluated:', fontsize=7)
lg.get_title().set_fontsize(7)
add_gridline(ax1)
ax1.set_xlabel('Iteration', fontsize=7)
ax1.set_ylabel('Total RMSN error', fontsize=7)
plt.savefig(save_path)
