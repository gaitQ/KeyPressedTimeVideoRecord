# -*- coding: utf-8 -*-
# Please consult Readme file for installing libraries

from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import  *
from PyQt5.QtCore import  *
from PyQt5.QtWidgets import *
from PyQt5 import sip
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow,QFileDialog,QListWidgetItem,QColorDialog
import sys
import sys, cv2, time
import os
import time
import qtawesome
videoTimeLabel=None
videoFileName =None
breakFlag = None
createTHFlag = True
videoPrograssSlider=None
videoCurrentPosition=0
videoLabelObject=None
file =None
timeflag=0
labelWidth=0
labelHeight=0
normalSpeedRadioButton=None 
halfSpeedRadioButton=None  
onefourthSpeedRadioButton=None  
numberFrames=None
font = cv2.FONT_HERSHEY_SIMPLEX
__flag=True
ui=None
isOpen=False
video_list=[]
frameTime = 32
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.newVerticalLayout = QtWidgets.QVBoxLayout(self.centralwidget) 
        self.newVerticalLayout.setObjectName("newVerticalLayout")
        global videoLabelObject
        videoLabelObject = QtWidgets.QLabel(self.centralwidget)
        videoLabelObject.setText("")
        videoLabelObject.setObjectName("videoLabelObject")
        self.newVerticalLayout.addWidget(videoLabelObject)
        global normalSpeedRadioButton,halfSpeedRadioButton,onefourthSpeedRadioButton
        normalSpeedRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        normalSpeedRadioButton.setObjectName("normalSpeedRadioButton")
        self.newVerticalLayout.addWidget(normalSpeedRadioButton)

        halfSpeedRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        halfSpeedRadioButton.setObjectName("halfSpeedRadioButton")
        self.newVerticalLayout.addWidget(halfSpeedRadioButton)
        halfSpeedRadioButton.setChecked(True)
        onefourthSpeedRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        onefourthSpeedRadioButton.setObjectName("onefourthSpeedRadioButton")

        self.newVerticalLayout.addWidget(onefourthSpeedRadioButton)

        self.fileOpenButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileOpenButton.setObjectName("fileOpenButton")
        self.newVerticalLayout.addWidget(self.fileOpenButton)

        global videoPrograssSlider
        videoPrograssSlider = QtWidgets.QPushButton(self.centralwidget)

        videoPrograssSlider.setObjectName("videoPrograssSlider")

        self.newVerticalLayout.addWidget(videoPrograssSlider)


        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setObjectName("nextButton")
        self.newVerticalLayout.addWidget(self.nextButton)
        self.videoPlayButton = QtWidgets.QPushButton(self.centralwidget)
        self.videoPlayButton.setObjectName("videoPlayButton")
        self.newVerticalLayout.addWidget(self.videoPlayButton)
        self.videoPauseButton = QtWidgets.QPushButton(self.centralwidget) 
        self.videoPauseButton.setObjectName("videoPauseButton")
        self.newVerticalLayout.addWidget(self.videoPauseButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.translateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.videoPlayButton.clicked.connect(self.videoPlay)
        self.videoPauseButton.clicked.connect(self.videoPause)

        self.fileOpenButton.clicked.connect(self.readFileContent)

        videoPrograssSlider.clicked.connect(self.resetVideo)
        self.nextButton.clicked.connect(self.nextVideo)

        QShortcut(QKeySequence("UP"),self.centralwidget,  self.recordU)
        QShortcut(QKeySequence("DOWN"), self.centralwidget, self.RecordDown)
        QShortcut(QKeySequence("Left"), self.centralwidget, self.recordL)
        QShortcut(QKeySequence("Right"), self.centralwidget, self.recordR)
        QShortcut(QKeySequence("SPACE"), self.centralwidget, self.playOrPause)
        
    def playOrPause(self):
        global videoPlayflag

        if videoPlayflag==True:

            videoPlayflag=False
            self.th.pause()
        else:
            time.sleep(2)
            print("Will Start Soon")
            videoPlayflag = True
            self.th.stopInitial()

    def translateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))
        self.fileOpenButton.setText(_translate("MainWindow", "Open"))
        self.videoPlayButton.setText(_translate("MainWindow", "Play"))
        self.videoPauseButton.setText(_translate("MainWindow", "Pause"))
        global videoPrograssSlider
        videoPrograssSlider.setText(_translate("MainWindow", "Start From Beginning"))
        global normalSpeedRadioButton, halfSpeedRadioButton, onefourthSpeedRadioButton
        normalSpeedRadioButton.setText(_translate("MainWindow", "Normal Speed"))
        halfSpeedRadioButton.setText(_translate("MainWindow", "1/2 Speed"))
        onefourthSpeedRadioButton.setText(_translate("MainWindow", "1/4 Speed"))
        self.nextButton.setText(_translate("MainWindow", "Next Video"))
        global createFlag,breakFlag,labelWidth,labelHeight,videoLabelObject
        createFlag = True
        breakFlag = False
        labelWidth=640
        labelHeight = 480

    def nextVideo(self):
        global video_list,videoFileName,breakFlag,createTHFlag
        if len(video_list) > 1:
            video_list = video_list[1:]
            videoFileName = video_list[0]

            createTHFlag = True
            if breakFlag == False and createTHFlag == True:
                breakFlag = True
                time.sleep(1)
                self.th = Thread(self.centralwidget)
                self.th.changePixmap.connect(self.setFrameImage)
                createTHFlag = True
                breakFlag = False
                global videoPlayflag
                videoPlayflag = True
                frameCapture = cv2.VideoCapture()
                frameCapture.open(videoFileName)
                print("name" + videoFileName)
                global videoCurrentPosition
                videoCurrentPosition = 0

                #numberFrames = int(frameCapture.get(cv2.CAP_PROP_FRAME_COUNT))

                self.th.start()
                #global file
                file = open(videoFileName+".txt", 'w+')
                file.write("")
                file.close()
                time.sleep(0.096)
                global __flag, isOpen
                __flag = False
                isOpen = True
                videoPlayflag = False

        else:
            video_list = []
            QMessageBox.information(self.centralwidget, "Processing Result", "this is the last video in the folder")

    def resetVideo(self):
        print("Call")
        global breakFlag, createTHFlag, videoFileName

        createTHFlag = True
        if breakFlag == False and createTHFlag == True:
            breakFlag = True
            time.sleep(1)
            self.th = Thread(self.centralwidget)
            self.th.changePixmap.connect(self.setFrameImage)
            createTHFlag = True
            breakFlag = False
            global videoPlayflag
            videoPlayflag = True
            frameCapture = cv2.VideoCapture()
            frameCapture.open(videoFileName)
            print("name" + videoFileName)
            global videoCurrentPosition
            videoCurrentPosition = 0

            numberFrames = int(frameCapture.get(cv2.CAP_PROP_FRAME_COUNT))

            self.th.start()
            global file
            file = open(videoFileName + ".txt", 'w+')
            file.write("")
            file.close()
            time.sleep(0.096)
            global __flag, isOpen
            __flag = False
            isOpen = True
            videoPlayflag = False


    def eventSizeChange(self):
        print("Changed")

    def readFileContent(self):
        directoryInitial =  QFileDialog.getExistingDirectory(self.centralwidget,'Select a File',"./")
        self.dir =  directoryInitial
        global video_list
        video_list=[]
        files = []
        video_type = ['mp4','avi','rmvb','flv']
        for root, dirs, files in os.walk(directoryInitial):
            break

        for item in files:
            if item[item.rfind(".") + 1:] in video_type:
                video_list.append(directoryInitial+"/"+item)
        print(video_list)
        global  videoFileName
        videoFileName = video_list[0]

        global breakFlag,createTHFlag
        createTHFlag = True
        if breakFlag ==False and createTHFlag == True:
            breakFlag = True
            time.sleep(1)
            self.th = Thread(self.centralwidget)
            self.th.changePixmap.connect(self.setFrameImage)
            createTHFlag = True
            breakFlag =False
            global videoPlayflag
            videoPlayflag=False
            frameCapture = cv2.VideoCapture()
            frameCapture.open(videoFileName)
            global numberFrames
            numberFrames = int(frameCapture.get(cv2.CAP_PROP_FRAME_COUNT))
            global frameTime
            frameTime = 1000.0/frameCapture.get(cv2.CAP_PROP_FPS) 

            global  videoCurrentPosition
            videoCurrentPosition = 0
            print("Start")
            self.th.start()
            global  file
            print(videoFileName[videoFileName.rfind("/"):]+"/")
            file = open(videoFileName+".txt", 'w+')
            file.write("")
            file.close()
            time.sleep(0.064)
            global __flag,isOpen
            __flag=False
            isOpen=True
            videoPlayflag=False
    def changeVideoPlayPosition(self):
        global breakFlag,createTHFlag

        if breakFlag ==False and createTHFlag == True:
            breakFlag = True
        time.sleep(1)
        self.th = Thread(self.centralwidget)
        self.th.changePixmap.connect(self.setFrameImage)
        createTHFlag = True
        breakFlag =False
        global videoPlayflag
        videoPlayflag=True
        frameCapture = cv2.VideoCapture()
        frameCapture.open(videoFileName)
        numberFrames = int(frameCapture.get(cv2.CAP_PROP_FRAME_COUNT))

        self.th.start()

        time.sleep(1)

        self.th.pause()

    def videoPause(self):

        global videoPlayflag 
        videoPlayflag = False
        self.th.pause()

    def videoPlay(self): 

        global videoPlayflag 
        videoPlayflag = True
        time.sleep(2)
        self.th.stopInitial()

    def setFrameImage(self, image):

        videoLabelObject.setPixmap(QPixmap.fromImage(image))
    def recordL(self):
        print("left button")
        ms = videoCurrentPosition*frameTime
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        print(ms)
        print("%02d:%02d:%02d:%03d" % (h, m, s,ms))
        time = "%02d:%02d:%02d:%03d" % (h, m, s,ms)

        #file = open(os.path.abspath(sys.argv[0]).replace("KeyPressedTimeVideoRecord.py","")+videoFileName[videoFileName.rfind("/"):] +".txt", 'a+')
        file = open(videoFileName +".txt", 'a+')
        file.write("L " +time + " \n")
        file.close()
    def recordR(self):
        print("right button")
        ms = videoCurrentPosition*frameTime
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        print(ms)
        print("%02d:%02d:%02d:%03d" % (h, m, s,ms))
        time = "%02d:%02d:%02d:%03d" % (h, m, s,ms)

        #file = open(os.path.abspath(sys.argv[0]).replace("KeyPressedTimeVideoRecord.py","")+videoFileName[videoFileName.rfind("/"):] +".txt", 'a+')
        file = open(videoFileName+".txt", 'a+')
        file.write("R "+time+ " \n")
        file.close()

    def recordU(self):
        print("up button")
        ms = videoCurrentPosition*frameTime
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        time = "%02d:%02d:%02d:%03d" % (h, m, s,ms)

        #file = open(os.path.abspath(sys.argv[0]).replace("KeyPressedTimeVideoRecord.py","")+videoFileName[videoFileName.rfind("/"):] +".txt", 'a+')
        file = open(videoFileName +".txt", 'a+')
        file.write("U "+time+ " \n")
        file.close()

    def RecordDown(self): 
        print("down button")
        ms = videoCurrentPosition*frameTime
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        time = "%02d:%02d:%02d:%03d" % (h, m, s,ms)
        
        #file = open(os.path.abspath(sys.argv[0]).replace("KeyPressedTimeVideoRecord.py","")+videoFileName[videoFileName.rfind("/"):] +".txt", 'a+')
        file = open(videoFileName+".txt", 'a+')
        file.write("D "+time+ " \n")
        file.close()
    def showMsg(self):
        QMessageBox.information(self.centralwidget, "Processing Result", "this is the last video in the folder")
class Thread(QThread):  
    changePixmap = pyqtSignal(QtGui.QImage)

    def run(self):
        global __flag,breakFlag,videoFileName,isOpen,videoLabelObject
        __flag = True
        frameCapture = cv2.VideoCapture(videoFileName)
        print(videoFileName)
        numberFrames = int(frameCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        print(numberFrames)
        self.sec = 0

        while (frameCapture.isOpened() == True):
            if breakFlag == True:
                break
            if __flag == True:
                ret, frame = frameCapture.read()
                self.frame_globe = frame

                if ret:
                    print("-------------++++++++++++")
                    global videoCurrentPosition

                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)

                    global videoLabelObject,labelHeight 
                    videoProportion= videoLabelObject.height() /labelHeight
                    p = convertToQtFormat.scaled(int(640*videoProportion), int(480*videoProportion), Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                    self.sec = self.sec + 1
                    print(self.sec)
                    global videoPrograssSlider
                    videoCurrentPosition = self.sec

                    global videoTimeLabel
                    m, s = divmod(int(videoCurrentPosition * frameTime/1000.0), 60)
                    h, m = divmod(m, 60)
                    global normalSpeedRadioButton, halfSpeedRadioButton, onefourthSpeedRadioButton
                    speedProportion=0 
                    if normalSpeedRadioButton.isChecked():
                        speedProportion=1
                    elif halfSpeedRadioButton.isChecked():
                        speedProportion = 2
                    elif onefourthSpeedRadioButton.isChecked():
                        speedProportion = 4
                    if int((frameCapture.get(cv2.CAP_PROP_FRAME_COUNT))-0.5) <=self.sec:
                        ms = videoCurrentPosition * frameTime
                        s, ms = divmod(ms, 1000)
                        m, s = divmod(s, 60)
                        h, m = divmod(m, 60)
                        print(ms)
                        print("%02d:%02d:%02d:%03d" % (h, m, s, ms))
                        timex = "%02d:%02d:%02d:%03d" % (h, m, s, ms)

                        file = open(videoFileName + ".txt", 'a+')
                        file.write("E " + timex + " \n")
                        file.close()
                    
                    if   isOpen ==True:
                        isOpen=False
                        self.pause()
                        
                    time.sleep(frameTime/1000.0*speedProportion)  

                else:
                    break
            else:
                time.sleep(0.5)

    def pause(self):
        global __flag
        __flag = False

        global img_frame, input_time, img_frame_t
        img_frame = self.frame_globe
        img_frame_t = self.frame_globe

    def resume(self):
        global __flag
        __flag.set()  

    def stopInitial(self):
        global __flag
        __flag = True
if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv) 
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_()) 