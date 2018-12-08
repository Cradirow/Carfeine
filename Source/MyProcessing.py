import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import csv
from scipy.interpolate import interp1d

# ECG 데이터 수집 csv/real-time
def acquire_data(file_name):
    f = open(file_name)
    csvReader = csv.reader(f)

    ecg_list = []
    for row in csvReader:
        ecg_list.append(float(row[0]))
        
    ecg_list = ecg_list[0:3000] # 30sec, 100Hz => 3000
    ecg_df = pd.Series(ecg_list)
    return ecg_df

def acquire_data():
    ser = serial.Serial("COM6", 115200) # port, baudrate
    ecg_list = []
    delay = 33 # 30sec, 100Hz => 3000

    t_end = time.time()+delay
    while time.time() < t_end:
        row = ser.readline().decode()
        ecg = float(row.split(',')[0])
        ecg_list.append(ecg)

    ecg_list = ecg_list[0:3000]
    ecg_df = pd.Series(ecg_list)
    ser.close()
    
    return ecg_df
    

# 100Hz 기준
def calc_avg(ecg_df):
    hrw = 0.75
    fs = 100
    mov_avg = []
    mov_avg = ecg_df.rolling(int(hrw*fs)).mean()
    avg_hr = np.mean(ecg_df)
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    mov_avg = [x*1.2 for x in mov_avg]
    return mov_avg
    
# R-정점 탐지
def detect_peak(ecg_df, mov_avg):
    window = []
    peak_list = []
    pos = 0

    for ecg in ecg_df:
        avg = mov_avg[pos]
        if (ecg < avg) and (len(window)<1):
            pos += 1
        elif ecg > avg:
            window.append(ecg)
            pos += 1
        else :
            maximum = max(window)
            r_peak = pos - len(window) + window.index(max(window))
            peak_list.append(r_peak)
            window = []
            pos += 1
    return peak_list

# RR-간격 계산
def calc_interval(peak_list):
    rr_list = []
    pos = 0
    while (pos<len(peak_list)-1):
        rr_interval = peak_list[pos+1]-peak_list[pos]
        ms_dist = rr_interval * 10.0 # 100Hz 기준
        rr_list.append(ms_dist)
        pos += 1
    return rr_list

# 심박수 계산
def calc_bpm(rr_list):
    bpm = 60000 / np.mean(rr_list)
    return bpm

# plot => 시간 영역
def plot_time(ecg_df, mov_avg, peak_list, bpm):

    pos_list = [ecg_df[x] for x in peak_list]
    
    plt.title("ECG - time domain")
    plt.plot(ecg_df, alpha = 0.5, color='black', label="ECG signal")
    plt.plot(mov_avg, color = 'orange', label='moving average')
    plt.scatter(peak_list, pos_list, color = 'red', label="BPM: %.1f" %bpm)
    plt.legend(loc=4, framealpha=0.6)
    plt.show()

# LF/HF 비 계산
def calc_ratio(ecg_df, peak_list, rr_list):
    rr_x = peak_list[1:]
    rr_y = rr_list
    rr_x_new = np.linspace(rr_x[0],rr_x[-1],rr_x[-1])
    f = interp1d(rr_x,rr_y,kind='cubic')

    n = len(ecg_df)
    frq = np.fft.fftfreq(len(ecg_df),d=((1/100))) #100Hz 기준
    frq = frq[range(n//2)]
    y = np.fft.fft(f(rr_x_new))/n
    y = y[range(n//2)]

    lf = np.trapz(abs(y[(frq>=0.04)&(frq<=0.15)]))
    hf = np.trapz(abs(y[(frq>=0.16)&(frq<=0.4)]))

    ratio = lf/hf
    return ratio

# plot => 주파수 영역
def plot_frq(ecg_df, peak_list, rr_list):
    rr_x = peak_list[1:]
    rr_y = rr_list
    rr_x_new = np.linspace(rr_x[0],rr_x[-1],rr_x[-1])
    f = interp1d(rr_x,rr_y,kind='cubic')
    
    n = len(ecg_df)
    frq = np.fft.fftfreq(len(ecg_df),d=((1/100))) # 100Hz 기준
    frq = frq[range(n//2)]
    y = np.fft.fft(f(rr_x_new))/n
    y = y[range(n//2)]

    plt.title("ECG - frequency domain")
    plt.xlim(0, 0.6)
    plt.ylim(0, 50)
    plt.plot(frq, abs(y))
    plt.xlabel("Hz")
    plt.show()

#===========================================================================
"""
ecg_df = acquire_data("C:\\Users\\jsh\\Desktop\\data.csv")
mov_avg = calc_avg(ecg_df)
peak_list = detect_peak(ecg_df, mov_avg)
rr_list = calc_interval(peak_list)
bpm = calc_bpm(rr_list)
plot_time(ecg_df,mov_avg,peak_list,bpm)
ratio = calc_ratio(ecg_df,peak_list,rr_list)
plot_frq(ecg_df, peak_list, rr_list)
"""

