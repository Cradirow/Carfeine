from pygame import mixer

def calc_median(ratio_list):
    ratio_list.sort()
    median = ratio_list[len(ratio_list)//2]
    return median

def alarm(median):
    mixer.init()
    if median < 0.45: # 0.45
        mixer.music.load("C:\\Users\\jsh\\Desktop\\step3.mp3")
        print("메시지3")
    elif median < 0.5: # 0.5
        mixer.music.load("C:\\Users\\jsh\\Desktop\\step2.mp3")
        print("메시지2")
    elif median < 0.55: # 0.55
        mixer.music.load("C:\\Users\\jsh\\Desktop\\step1.mp3")
        print("메시지1")
    else:
        return
    
    mixer.music.play()

