# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 14:39:19 2021

@author: didit
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

#Changable Inputs ---------------------------------------------------------
file_loc = "C:/Users/didit/Desktop/BMEN 207/PPG_data/Data_"
start_file = 6
end_file = 8

thresholdMag = .1 #10% threshold from mean
sample_rate = 100 #samples/sec
lookback_time = 10 #seconds

#--------------------------------------------------------------------------------

#importing data from files
def read_data_files(file_prefix, start_file_num, end_file_num):
    """
    
    Parameters
    ----------
    file_prefix: the file location of the data all the way up to the number of the data (the 'file_num')
    start_file_num: the number of the first data file (lower number)
    end_file_num: the number of the last data file (higher number)
    
    
    Returns
    -------
    one dataframe with all data appended together.

    """
    file_extension = ".csv"
    file_list = []
    
    #This loop adds all the data files inbetween the start and end numbers to a list
    i = start_file_num
    for i in range(0,(end_file_num - start_file_num + 1)):
        file_list.append(file_prefix+str(start_file_num+i)+file_extension)
        if start_file_num == end_file_num:
            break
    
    #This loop reads in all the data files and then turns them into one dataframe
    for j in range(0,len(file_list)):
        df = pd.read_csv(file_list[j])
        if j == 0:
            dfFinal = df
            continue
        dfFinal = dfFinal.append(df, ignore_index=True)
        
    return dfFinal
data = read_data_files(file_loc, start_file, end_file)


accX = data[' Acc X']
accY = data[' Acc Y']
accZ = data[' Acc Z']
red = data[' Red (L)']
ir = data[' IR (L)']

#calculating normalized magnitude
magnitude = (accX**2 + accY**2 + accZ**2)**(1/2)
mean = np.mean(magnitude)
normal_mag = magnitude/mean
upperThresh = 1 + thresholdMag
lowerThresh = 1 - thresholdMag

#lookback sampling -------------------------------------------------------------
lookback_size = sample_rate * lookback_time
activity = np.zeros(len(normal_mag))
activity_final = np.zeros(len(normal_mag))
x_vals = [] # x-values used in plot

for a,b in enumerate(normal_mag): #if data is within the threshold, it is low activity (1), otherwise its high activity(0)
    x_vals.append(a)   
    if (b <= upperThresh and b >= lowerThresh): 
        activity[a] = 1 

for i in range(lookback_size,len(activity)): #finds periods of low activity using a moving window
    window = activity[i-lookback_size:i]
    if np.count_nonzero(window) == lookback_size:
        activity_final[i-lookback_size:i] = 1

        
percent_in_threshold = np.count_nonzero(activity_final) / len(activity_final)
print('Percentage of time not active:', round(percent_in_threshold*100, 2), '\b%')


#___________________________PLOT________________________________________________
plt.rcParams.update({'font.size':8})
plt.plot(x_vals, normal_mag, label='Magnitude', linewidth=.5)
#plt.axhline(y=upperThresh, color='r', linestyle='--', linewidth=.5)
#plt.axhline(y=lowerThresh, color='r', linestyle='--', label='Threshold', linewidth=.5)
plt.plot(x_vals, activity_final, label='Within +/- 10% of Mean Magnitude', linewidth=1)
plt.title('Magnitude vs Time (Files: '+ 'Data_{}'.format(start_file)+ ' to Data_{})'.format(end_file))
plt.xlabel('time (ms)')
plt.ylabel('Normalized Magitude')
plt.legend(loc='best')
plt.show()













