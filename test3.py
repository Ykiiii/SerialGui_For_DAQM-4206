import numpy as np
import pyqtgraph as pg
import sys,time
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt,QTimer
import pandas as pd
from Gdate import creatdata
from getSerialData import get_serialData



class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.generate_image()
        self.show_flag = False
        self.A = 818


    def initUI(self):
        self.setGeometry(200,200,1000,800)
        self.setWindowTitle("实时测量值")
        self.gridLayout = QGridLayout(self)
        self.frame = QFrame(self)
        # self.frame.setFrameShape(QFrame.Panel)
        # self.frame.setFrameShadow(QFrame.Plain)
        # self.frame.setLineWidth(2)
        self.frame.setStyleSheet("background-color:rgb(255,255,255);")
        self.label = QLabel(self)
        self.label.setText("测量数值")
        self.label.setAlignment(Qt.AlignCenter)
        # self.button = QPushButton(self)
        # self.button.setText("生成波形图")
        # self.button.clicked.connect(self.btnClick)

        self.startBtn = QPushButton('开始')
        self.endBtn = QPushButton('结束')

        self.combobox = QComboBox()
        self.combobox.addItems(["com1", "com2", "com3", "com4", "com5"])
        self.combobox.currentIndexChanged.connect(self.seleCOMchange)

        self.gridLayout.addWidget(self.frame,0,0,1,2)
        self.gridLayout.addWidget(self.label,1,0,1,1)
        self.gridLayout.addWidget(self.combobox,1,1,1,1)
        # self.gridLayout.addWidget(self.button,1,2,1,1)
        self.gridLayout.addWidget(self.startBtn, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.endBtn,   2, 1, 1, 1)

        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)

        self.setLayout(self.gridLayout)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.plotData)

        self.serCom = 'com1'

    def seleCOMchange(self):
        self.serCom = self.combobox.currentText()


    def generate_image(self):
        verticalLayout = QVBoxLayout(self.frame)
        win = pg.GraphicsLayoutWidget(self.frame)
        verticalLayout.addWidget(win)
        p = win.addPlot(title="动态波形图")
        p.showGrid(x=True,y=True)
        p.setLabel(axis="left",text="num / 1")
        p.setLabel(axis="bottom",text="t / s")
        p.setTitle("数据实时曲线")
        p.addLegend()

        self.curve1 = p.plot(pen="g",name="测量值")
        # self.curve2 = p.plot(pen="g",name="y2")

        self.Fs = 840.0 #采样频率
        self.N = 840    #采样点数
        self.f0 = 4.0    #信号频率
        self.pha = 0     #初始相位
        # self.t = np.arange(self.N) / self.Fs    #时间向量 1*1024的矩阵
        self.t = creatdata(self.N)
        self.y = np.zeros((self.N))


    def plotData(self):
        # I_data = int(get_serialData(self.serCom, 9600)[0])
        V_data = int(get_serialData(self.serCom, 9600))
        V_result = ((V_data - self.A) * (10 - 0.45) / (4095 - 819)) * 697837.0616 + 628.9686
        V_result = V_result / 3.6e9
        # print(self.A,V_data,V_data - self.A)
        # print(self.t)
        self.A = V_data
        self.label.setText(str(V_result)+'M3·s-1') #实时数据

        self.pha += 10
        self.t = creatdata(self.N)
        self.y = np.append(self.y[1:],V_result)
        self.curve1.setData(self.t , self.y)  #实时曲线
        # self.curve2.setData(self.t , np.cos(8 * np.pi  * self.t + self.pha * np.pi/180.0))
        # 打印当前数据
        # print(self.y)



    # def show_data(self):


    def btnClick(self):
        self.button.setText(str(self.show_flag))
        self.show_flag = not (self.show_flag)
        print(self.show_flag)



    def startTimer(self): #设置时间间隔并启动定时器
        self.timer1.start(1000)
        #设置开始按钮不可点击，结束按钮可点击
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)
    def endTimer(self): #停止定时器
        self.timer1.stop() #结束按钮不可点击，开始按钮可以点击
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())