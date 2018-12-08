from PyQt4.QtGui import *
import threading
import time
import sys

# GUI 모듈
import MyDiag

# Processing 모듈 
from MyProcessing import *
# Analysis 모듈
from MyAnalysis import *


def run():
        #ecg_df = acquire_data("C:\\Users\\jsh\\Desktop\\data.csv")
        median_list = []
        while (len(median_list) < 6):
            ratio_list = []
            while(len(ratio_list) < 10): # 5분 ratio 데이터(10)
                ecg_df = acquire_data() # 30초 ecg 데이터(3000)
                mov_avg = calc_avg(ecg_df)
                peak_list = detect_peak(ecg_df, mov_avg)
                rr_list = calc_interval(peak_list)
                bpm = calc_bpm(rr_list)
                ratio = calc_ratio(ecg_df,peak_list,rr_list)
                ratio_list.append(ratio)
            
                print(ratio,",",bpm)

            median = calc_median(ratio_list)
            print("Ratio median :",str(median))
            alarm(median)
            median_list.append(median)
        plt.plot(median_list)
        plt.show()

# GUI class
class XDialog(QDialog, MyDiag.Ui_myDialog):
    def __init__(self):
        QDialog.__init__(self)

        # 임시 애니메이션 - 삭제해도 무방 
        self.movie = QMovie("C:\\Users\jsh\\Desktop\\heart-signal.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.setupUi(self)

        # 시작버튼 핸들러
        self.myBtn.clicked.connect(self.clickBtn)
        self.flag = True
        
    def clickBtn(self):
        if self.flag == True:
            self.flag = False # 시작 => 종료
            self.myBtn.setText("종료")

            # 쓰레드
            t = threading.Thread(target=run)
            t.daemon = True
            t.start()
            
        else:
            self.flag = True # 종료
            sys.exit(1)

        
    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)


app = QApplication(sys.argv)
dlg = XDialog()
dlg.show()
app.exec_()

