# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 18:54:04 2021

@author: didit
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from datetime import datetime
import time
from operator import truediv

#Changable Inputs ---------------------------------------------------------------
FILE_LOC = "C:/Users/didit/Desktop/BMEN 207/PPG_data/Data_"
START_FILE = 6
END_FILE = 60

THRESHOLD_MAG = .1 #10% threshold from mean
SAMPLE_RATE = 100 #samples/sec
LOOKBACK_TIME = 10 #seconds


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
data = read_data_files(FILE_LOC, START_FILE, END_FILE)

accX = data[' Acc X']
accY = data[' Acc Y']
accZ = data[' Acc Z']
red = data[' Red (L)']
ir = data[' IR (L)']

#Thresholds
upperThresh = 1 + THRESHOLD_MAG
lowerThresh = 1 - THRESHOLD_MAG

#convert unix time into readable time
data[' Time'] = pd.to_datetime(data[' Time'], unit='s').astype(str)

#magnitude, mean, normalized magnitude, and standard deviation 
magnitude = (accX**2 + accY**2 + accZ**2)**(1/2)
mean = np.mean(magnitude)
normal_mag = magnitude/mean
stdev = np.std(magnitude)

#adding normalized magnitude to the dataframe
normal_mag_list = []
for i in magnitude:
    normal_mag_list.append(i/mean)
data['Normal Mag'] = normal_mag_list



#lookback sampling -------------------------------------------------------------------
lookback_size = SAMPLE_RATE * LOOKBACK_TIME
activity = np.zeros(len(normal_mag))
activity_final = np.zeros(len(normal_mag))
x_vals = [] # x-values used in 'high and low activity plot'

for a,b in enumerate(normal_mag): #if data is within the threshold, it is low activity (1), otherwise its high activity(0)
    x_vals.append(a)   
    if (b <= upperThresh and b >= lowerThresh): 
        activity[a] = 1 

for i in range(lookback_size,len(activity)): #finds periods of low activity using a moving window
    window = activity[i-lookback_size:i]
    if np.count_nonzero(window) == lookback_size:
        activity_final[i-lookback_size:i] = 1
        
percent_in_threshold = np.count_nonzero(activity_final) / len(activity_final)

#low activity data dataframe 
low_act_bool = map(bool, activity_final)
low_act_filtr = pd.DataFrame(low_act_bool)
low_act_data = data.loc[low_act_filtr[0], [' Time', ' Red (L)', ' IR (L)', 'Normal Mag']]
#-------------------------------------------------------------------------------------

#Counting number of low and high activity periods-------------------------------------
low_act_mag = []
prior_num = 0
high_act_count = 1 # starts at 1 because the loop only counts when activity_final switches between high and low activity. It will always start at high activity
low_act_count = 0
for j in range(0, len(activity_final)):
    transition = str(int(prior_num)) + str(int(activity_final[j]))
    prior_num = activity_final[j]
    if transition == '01':
        high_act_count += 1
    if transition == '10':
        low_act_count += 1
#-------------------------------------------------------------------------------------



#HR-----------------------------------------------------------------------------------
h = None
t = None
p = 500
w = 10
hr_conversion = 100 * 60
red_AC = []
ir_AC = []
R = []
SpO2 = []


red_trough    = -(red - np.mean(red))
redPEAKS, _   = find_peaks(red, height=h, threshold=t, prominence=p, width=w)
redTROUGHS, _ = find_peaks(red_trough, height=h, threshold=t, prominence=p, width=w)
delta_red     = np.diff(redPEAKS)
avg_delta_red = np.mean(delta_red)
BPM_red       = (1/avg_delta_red) * hr_conversion

ir_trough    = -(ir - np.mean(ir))
irPEAKS, _   = find_peaks(ir, height=h, threshold=t, prominence=p, width=w)
irTROUGHS, _ = find_peaks(ir_trough, height=h, threshold=t, prominence=p, width=w)
delta_ir     = np.diff(irPEAKS)
avg_delta_ir = np.mean(delta_ir)
BPM_ir       = (1/avg_delta_ir) * hr_conversion

BPM = (BPM_red + BPM_ir) / 2

red_peaks   = [red[redPEAKS[i]] for i in range(0,len(red[redPEAKS]))]
# print(redPEAKS)
red_troughs = [red[redTROUGHS[i]] for i in range(0, len(red[redTROUGHS]))]
ir_peaks    = [ir[irPEAKS[i]] for i in range(0,len(ir[irPEAKS]))]
ir_troughs  = [ir[irTROUGHS[i]] for i in range(0, len(ir[irTROUGHS]))]



red_peaks = np.zeros(len(data))
# if red_peaks[i] 
for i in range(len(data)):
    if redPEAKS[i] == i:
        red_peaks[i] = red[redPEAKS[i]]


print(red_peaks)










   
red_AC = list(set(red_peaks) - set(red_troughs))
red_DC = red_troughs

ir_AC = list(set(ir_peaks) - set(ir_troughs))
ir_DC = ir_troughs

R_red = list(map(truediv, red_AC, red_DC)) #red_AC / red_DC
R_ir = list(map(truediv, ir_AC, ir_DC))    #ir_AC / ir_DC
R = list(map(truediv, R_red, R_ir))        #R_red / R_ir
R_reverse = [1 / R for R in R]             #1/R
SpO2 = [(129 - R_reverse * 32) for R_reverse in R_reverse]         #129- R*32    
# print(len(SpO2))
# print(len(data))
# for i in range(0, len(SpO2)):
#     if SpO2[i] > 100:
#         SpO2 = np.delete(SpO2, i)
#     if SpO2[i] < 80:
#         SpO2 = np.delete(SpO2, i)

# print(SpO2)
"""
#_____________________________PLOT________________________________________
plt.plot(redPEAKS, red[redPEAKS], 'o', linewidth=10, markersize=5)
plt.plot(redTROUGHS, red[redTROUGHS], '*', linewidth=10, markersize=5)
# plt.plot(irPEAKS, ir[irPEAKS], 'o', linewidth=10, markersize=5)
# plt.plot(irTROUGHS, ir[irTROUGHS], '*', linewidth=10, markersize=5)
plt.ylabel('ADC Counts')
plt.xlabel('time (ms)')
plt.title('Heart Rate by Peak Detection (Red of Data 6-80.csv)')
# plt.xlim(200,1400)
# plt.ylim(183000, 187000)
plt.show()
"""




#-------------------------------------------------------------------------------------





#________________________CONSOLE OUTPUTS____________________________________________

# #high and low activity count
# print('Number of high activity periods: ', high_act_count)
# print('Number of low activity periods:  ', low_act_count)

# #HR from HR and IR data
# print("The heartrate is: ", BPM, "BPM")

# # % of low activity time
# print('Percentage of time not active:', round(percent_in_threshold*100, 2), '\b%')

#_____________________________________________________________________________________
"""
#____________________________________HIGH AND LOW ACTIVITY PERIODS PLOT_______________________________________
plt.rcParams.update({'font.size':8})
plt.plot(x_vals, normal_mag, label='Magnitude', linewidth=.5)
#plt.axhline(y=upperThresh, color='r', linestyle='--', linewidth=.5)
#plt.axhline(y=lowerThresh, color='r', linestyle='--', label='Threshold', linewidth=.5)
plt.plot(x_vals, activity_final, label='Within +/- 10% of Mean Magnitude', linewidth=1)
plt.title('Magnitude vs Time (Files: '+ 'Data_{}'.format(START_FILE)+ ' to Data_{})'.format(END_FILE))
plt.xlabel('time (ms)')
plt.ylabel('Normalized Magitude')
#plt.legend(loc='best')
plt.show()
#______________________________________________________________________________________________________________
"""


#________________________________HR PLOT W/ ERROR BARS________________________________________________







