# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 14:26:55 2021

@author: didit
"""

import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import time

t_initial = time.time()

def read_data_files(file_prefix, start_file_num, end_file_num):
    """
    
    Parameters
    ----------
    file_prefix: the prefix to the data files
    start_file_num: the number on the first data file (lower number)
    end_file_num: the number on the last data file (higher number)
    
    
    Returns
    -------
    one dataframe with all data appended together.

    """
    #This loop adds all the data files inbetween the start and end numbers to a list
    file_list = []
    i = start_file_num
    for i in range(0,(end_file_num - start_file_num + 1)):
        file_list.append(file_prefix+str(start_file_num+i))
    
    #This loop reads in all the data files and then turns them into one dataframe
    for j in range(0,len(file_list)):
        df = pd.read_csv('C:/Users/didit/Desktop/BMEN 207/PPG_data/{0}.csv'.format(file_list[j]))
        if j == 0:
            dfFinal = df
            continue
        dfFinal = dfFinal.append(df, ignore_index=True)
    return dfFinal
data = read_data_files("Data_",6,163)

#converts Unix time into readable time
time_data = []
for i in range(0,len(data)):
    t = int(data.loc[i,' Time'])
    time_data.append(datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'))
data.loc[:,' Time'] = time_data # saves readable time in the Time column in data


#parsing through the hours ------------------------------------
std_list = [] #standard deviation list
hour_list = [] #hours list (0-23)
mag_list = [] #magnitude list

for hour in range(0,24):
    hour_list.append(hour)
    if hour < 10:
        hr_str = ' 0' + str(hour) + ':'
    else:
        hr_str = ' ' + str(hour) + ':'
        
    filtr = (data[' Time'].str.contains(hr_str))
    #a = filtr.value_counts()
        #NO DATA IN HOUR = 7 to HOUR = 20
   
    acc_data = data.loc[filtr,[' Time',' Acc X',' Acc Y',' Acc Z']]
    mag = (acc_data[' Acc X']**2 + acc_data[' Acc Y']**2 + acc_data[' Acc Z']**2).pow(1/2) # magnitude
    stdev = np.std(mag) # standard deviation
    std_list.append(stdev)
    if np.isnan(stdev) != True:
        mag_list.append(mag)

std_list = [0 if stdev != stdev else stdev for stdev in std_list] # turns all NaNs into 0s
#print(mag_list)  <--- used to find most active day (longest length)

# PLOT ------------------------------------------------    
plt.plot(hour_list, std_list)
plt.ylabel('STD of Magnitude')
plt.xlabel('Hours')
plt.title('Activity By Hour')
plt.show()

fig2 = plt.figure()
new_plot = fig2.add_subplot(111)
bin_edges = [1600,1700,1800,1900,2000,2100,2200,2300,2400]
n, bins, patches = new_plot.hist(mag_list[8], bins=bin_edges, density=False, facecolor='g', alpha=.85)
new_plot.set_xlabel('Acc Magnitude')
new_plot.set_ylabel('Counts')
new_plot.set_title('Histogram of Acc Magnitudes of Most Active Hour')

t_final = time.time()
print("Run Time:", str(t_final-t_initial), "\bs")
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
    
    
    
    
    
    
    