# plot용 모듈

import sys
# Processing 모듈
from MyProcessing import *

ratio_list = []
while(len(ratio_list) < 10): # 10box => 5분
    ecg_df = acquire_data()
    mov_avg = calc_avg(ecg_df)
    peak_list = detect_peak(ecg_df, mov_avg)
    rr_list = calc_interval(peak_list)
    bpm = calc_bpm(rr_list)

    plot_time(ecg_df,mov_avg, peak_list, bpm) # 시간 영역

    ratio = calc_ratio(ecg_df,peak_list,rr_list)
    ratio_list.append(ratio)
    print(ratio,",",bpm)

    plot_frq(ecg_df,peak_list, rr_list) # 주파수 영역
