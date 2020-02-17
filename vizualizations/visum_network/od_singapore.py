'''
Created on 11 Feb 2020

@author: thenuwan.jayasinghe
@note: to visualize the distribution of the values in the OD matrix
'''

import pandas as pd
import matplotlib.pyplot as plt

od_file_path = "C:\\Users\\thenuwan.jayasinghe\\OneDrive - tum.de\\Thesis\\3_Analysis\\HB_Assignment_10_Day\\OD Matrix\\ODPAIR.txt"
col_names = ['From', 'To', 'Volume', 'Diagonal']

od_data = pd.read_csv(od_file_path, header = None, names = col_names)

zeros = od_data['Volume'] == 0
below_ten = od_data['Volume'] <= 10
#===============================================================================
# print zeros.sum()
# print od_data['Volume'].sum()
# print below_ten.sum()
# print od_data['Volume'].describe()
#===============================================================================

plt.hist(od_data['Volume'], normed=True, cumulative=True, histtype='step')
plt.show()
#print od_data['Volume'].max()
#plt.show()

#Visualization

#===============================================================================
# od_data['Volume'].plot.hist()
# plt.show()
#===============================================================================