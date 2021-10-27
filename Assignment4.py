# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 22:25:17 2021

@author: didit
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks

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
        if start_file_num == end_file_num:
            break
    
    #This loop reads in all the data files and then turns them into one dataframe
    for j in range(0,len(file_list)):
        df = pd.read_csv('C:/Users/didit/Desktop/BMEN 207/PPG_data/{0}.csv'.format(file_list[j]))
        if j == 0:
            dfFinal = df
            continue
        dfFinal = dfFinal.append(df, ignore_index=True)
    return dfFinal
data = read_data_files("Data_",6,6)

ir = data[' IR (L)'][:]
red = data[' Red (L)'][:]
plt.plot(red)
ir_trough = -(ir - np.mean(ir))
red_trough = -(red - np.mean(red))


peak_h = None
peak_t = None
peak_p = 500
peak_w = 10

irPEAKS, _ = find_peaks(ir, height = peak_h, threshold = peak_t, prominence = peak_p, width = peak_w)
irTROUGHS, _ = find_peaks(ir_trough, height = peak_h, threshold = peak_t, prominence = peak_p, width = peak_w)
redPEAKS, _ = find_peaks(red, height = peak_h, threshold = peak_t, prominence = peak_p, width = peak_w)
redTROUGHS, _ = find_peaks(red_trough, height = peak_h, threshold = peak_t, prominence = peak_p, width = peak_w)

delta_red = np.diff(redPEAKS)
avg_delta_red = np.mean(delta_red)
delta_ir = np.diff(irPEAKS)
avg_delta_ir = np.mean(delta_ir)

hr_conversion = 100 * 60
BPM_red = (1/avg_delta_red) * hr_conversion
BPM_ir = (1/avg_delta_ir) * hr_conversion
print("The heartrate from the Red(L) data is:", BPM_red, "BPM")
print("The heartrate from the IR(L) data is:", BPM_ir, "BPM")

#_____________________________PLOT________________________________________
plt.plot(redPEAKS, red[redPEAKS], 'o', linewidth=10, markersize=5)
plt.plot(redTROUGHS, red[redTROUGHS], '*', linewidth=10, markersize=5)
plt.ylabel('ADC Counts')
plt.xlabel('t(ms)')
plt.title('Heart Rate by Peak Detection (Red of Data_6.csv)')
plt.xlim(200,1400)
plt.ylim(183000, 187000)
plt.show()



















