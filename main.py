# -*- coding: UTF-8 -*-
# TODO 清空无用的import
import threading
import urllib.request
import websocket
import simplejson as json
import qrcode
import os
from moviepy.editor import VideoFileClip
import scan_dialog_ui 
import player_ui
import wait_select_ui
import result_ui
import math
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer,QCamera,  QCameraImageCapture

from PyQt5.QtMultimediaWidgets import QVideoWidget,QCameraViewfinder
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction,QGraphicsScene,QGraphicsView
from PyQt5.Qt import QImage,QPixmap
import sys
import cv2,time


SERVER_URL = "ws://dev-accwssail.healthmall.cn/server/bodyAnaylzer/data"
MID = "0001"

# 声明用户信息为全局变量
memberId = ""
memberName = ""
memHeadImg = ""
sectionList = ""
courseName = ""

# 连续播放的次数
play_times = 0
# 初始界面
class Scan_dialog(QtWidgets.QDialog, scan_dialog_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(Scan_dialog, self).__init__()
        global memHeadImg
        global memberName
        global memberId

        # TODO 初始化个人信息
        memberName = ""
        memberId = ""
        memHeadImg = ""

        # 生成二维码
        qrcodeInfo = "https://accwsiot.healthmall.cn/unAppOpen?id=AR" + MID

        self.setupUi(self) 

        self.make_qr(qrcodeInfo)

        # 更新qrc文件
        os.system('pyrcc5.exe res.qrc -o res_rc.py')

        # 替换二维码图片
        self.widget.setStyleSheet("background:white;\n"
        "image: url(:/img/AR教学视频v1.0/res/theqrcode.png);")

    def make_qr(self, str):
        qr = qrcode.QRCode(version=5,  # 生成二维码尺寸的大小 1-40 1:21*21（21+(n-1)*4）
                           error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
                           box_size=10,  # 每个格子的像素大小
                           border=2,  # 边框的格子宽度大小
                           )
        qr.add_data(str)
        qr.make(fit=True)
        img = qr.make_image()
        img.save("AR教学视频v1.0/res/theqrcode.png")

class Wait_ui(QtWidgets.QDialog,wait_select_ui.Ui_Dialog):
    def __init__(self):
        super(Wait_ui, self).__init__()
        self.setupUi(self)

class Player_ui(QtWidgets.QDialog,player_ui.Ui_Dialog):
    def __init__(self):
        super(Player_ui, self).__init__()
        self.setupUi(self)

class Result_ui(QtWidgets.QDialog,result_ui.Ui_Dialog):
    def __init__(self):
        super(Result_ui, self).__init__()
        self.setupUi(self)

        # TODO 自动加锁时间需要调整
        self.timer_result = QtCore.QTimer()
        self.timer_result.timeout.connect(self.auto_finish)
        self.timer_result.start(5 * 1000)

    def auto_finish(self):
        j.jump(["jumpToScan", ])

# 创建跳转对象
class Jump_to(object):
    def __init__(self):
        pass

    def jump(self, messList):
        global memHeadImg
        global memberName
        global memberId
        global sectionList
        global courseName

        command = messList[0]

        if command == "jumpToScan":
            # 关闭上层窗口,防止异常添加保护
            try:
                if self.w2.isVisible():
                    self.w2.reject()
                elif self.w3.isVisible():
                    self.w3.reject()
                elif self.w4.isVisible():
                    self.w4.reject()
            except Exception:
                print(Exception)

            # 判断是否在视频播放阶段
            try:
                self.player.pause()
            except Exception:
                print(Exception)
            w.exec_()

        elif command == "jumpToWait":
            # 关闭上层窗口
            w.reject()

            self.w2 = Wait_ui()
            self.w2.exec_()

        elif command == "jumpToPlay":
            self.jump_to_play()

        elif command == "jumpToResult":
            self.jump_to_result()

    def jump_to_result(self):
         # 关闭上层窗口
        self.w3.reject()

        # TODO 完善下面这句代码
        self.player.pause()

        self.w4 = Result_ui()
        self.w4.exec_()

    def jump_to_play(self):

        # 关闭上层窗口
        self.w2.reject()
        self.w3 = Player_ui()

        # 保存学生头像，覆盖默认图片
        path = os.getcwd() + '/AR教学视频v1.0/res/user_icon.jpg'
        urllib.request.urlretrieve(memHeadImg, path)

        # 设置学生头像
        self.w3.user_icon.setStyleSheet("border-image: url(:/img/AR教学视频v1.0/res/user_icon.jpg);\n"
    "border:NONE\n")

        # TODO 需要老师名称和头像地址
        self.w3.tech_name.setText("<html><head/><body><p><span style=\" font-size:26pt; color:#ffffff;\">陈老师</span></p></body></html>")
        self.w3.course_name.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#fff;\">"+courseName+"</span></p></body></html>")
        self.w3.cal_num.setText("<html><head/><body><p><span style=\" font-size:42pt; color:#fff;\">320</span><span style=\" font-size:22pt; color:#939a99;\">千卡</span></p></body></html>")
        self.w3.user_name.setText( "<html><head/><body><p><span style=\" font-family:\'PingFang SC\'; font-size:26pt; color:#ffffff;\">"+memberName+"</span></p></body></html>")
        self.w3.goal_num.setText("<html><head/><body><p><span style=\" font-size:42pt; color:#fff;\">89</span><span style=\" font-size:22pt; color:#939a99;\">/100分</span></p></body></html>")

        # 加上视频播放功能
        fileNameList = [os.getcwd()+'\some2.mp4', os.getcwd()+'\some3.mp4',]

        self.player = VideoWindow()

        # 初始化播放时长,向上取整
        self.duration = math.ceil(self.player.getDuration(fileNameList))
        timer_text = ("%02d:%02d" % (self.duration / 60, (self.duration % 60)))
        self.w3.time.setText("<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">" + str(timer_text) + "</span></p></body></html>")

        # 初始化定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer_display)

        # 开始播放,开启倒计时
        self.player.play(fileNameList)
        self.timer.start(1000)
        #开启摄像头
        self.player.camera_start()
        self.w3.horizontalLayout_2.addWidget(self.player.videoWidget)
        self.w3.horizontalLayout_2.addWidget(self.player.cameraviewfinder)

        # 设置居中平分
        self.w3.horizontalLayout_2.setStretch(0, 1)
        self.w3.horizontalLayout_2.setStretch(1, 1)

        self.w3.exec_()

    def update_timer_display(self):
        self.duration = self.duration - 1

        timer_text = ("%02d:%02d" % (self.duration / 60, (self.duration % 60)))
        self.w3.time.setText("<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">" + str(timer_text) + "</span></p></body></html>")

        # 播放结束后自动跳转
        if self.duration == 0:
            if self.w3.isVisible():
                self.jump_to_result()

# 创建服务器连接
class recv_socket(QThread):
    # 声明信号，发送信号时传入list
    trigger = pyqtSignal(list)

    def __init__(self):
        super(recv_socket,self).__init__()
        pass

    # QThread的第二线程
    def run(self):
        # 创建连接
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(SERVER_URL ,
               on_message = self.on_message,
               on_error = self.on_error,
               on_close = self.on_close
                )

        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, ws, message_server):
        # TODO 改变跳转传入参数

        # 声明全局变量
        global memberId
        global memHeadImg
        global memberName
        global courseName
        global sectionList

        # json转化为dict
        dict_message = json.loads(message_server)

        message = dict_message["message"]
        print(message)

        if message == "register success":
            pass
            # TODO 需要一些保护机制

        elif message == "register failed": 
            pass

        # 解锁界面
        elif message == "unlock":
            memberId = dict_message["memberId"]
            memberName = dict_message["memberName"]
            memHeadImg = dict_message["memHeadImg"]

            # 页面跳转
            # 数据形式为跳转命令+传入参数
            messList = ["jumpToWait", memberId, memberName, memHeadImg]
            self.emit_signal(messList)

            # 以json形式返回message
            send_message = {"message": "unlock ok"}
            ws.send(json.dumps(send_message))
        
        elif message == "lock":
            print("返回二维码界面")

            # 发送跳转信号
            messList = ["jumpToScan",]


            self.emit_signal(messList)
            send_message = {"message": "lock ok"}
            ws.send(json.dumps(send_message))

        elif message == "executeList":
            print("启动视频")

            sectionList = dict_message["sectionList"]
            courseName = dict_message["courseName"]

            # 发射参数为命名+课程List+课程名称
            messList = ["jumpToPlay", sectionList, courseName]
            self.emit_signal(messList)

            # 以json形式返回message
            send_message = {"message": "executeList ok"}
            ws.send(json.dumps(send_message))

        elif message == "closure":
            print("结束视频")
            messList = ["jumpToResult", ]

            # 发送跳转信号
            self.emit_signal(messList)

            # 以json形式返回message
            send_message = {"message": "closure ok"}

            ws.send(json.dumps(send_message))

        #TODO 长连接断开后需要自动建立连接
      
    def on_error(self, ws, error):
        print(error)

    def on_open(self, ws):
        # 发送机器唯一标识码
        ws.send("{\"message\":\"register\",\"deviceID\":\"AR000001\"}")

    def on_close(self, ws):
        print("close:")
        print(ws)

    # 发射信号
    def emit_signal(self, messList):
        self.trigger.emit(messList)

# 视频播放
class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)

        global play_times
        play_times = 0

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.camera = QCamera(0)
        self.cameraviewfinder = QCameraViewfinder()
        self.cameramode = self.camera.CaptureMode(2)
        self.cameraimgcap = QCameraImageCapture(self.camera)
        self.videoWidget = QVideoWidget()

        self.scene1 = QGraphicsScene()
        self.view1 = QGraphicsView(self.scene1)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.cameraviewfinder.show()
        self.camera.setViewfinder(self.cameraviewfinder)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self, fileNameList):
        self.fileNameList = fileNameList
        self.play_next()

    def play_next(self):
        global play_times

        if play_times >= len(self.fileNameList):
                self.timer_play.stop()
                return

        single_file = self.fileNameList[play_times]

        if single_file != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(single_file)))

        self.mediaPlayer.play()

        # 开启倒计时,进行连续播放
        single_time = math.ceil(self.getDuration(single_file))

        self.timer_play = QtCore.QTimer()
        self.timer_play.timeout.connect(self.play_next)

        # 定时器以毫秒作为单位
        self.timer_play.start(single_time * 1000)
        play_times = play_times + 1

    def camera_start(self):
        # 开启摄像头
        self.cameraviewfinder.resize(640, 480)
        self.camera.start()

    # 获取视频时长(单位为秒)
    def getDuration(self,fileName):
        total_times = 0

        if type(fileName) != list:
            clip = VideoFileClip(fileName)
            return clip.duration
        for f in fileName:
            clip = VideoFileClip(f)
            times = clip.duration
            total_times = total_times + times

        return total_times

    def pause(self):
       self.mediaPlayer.pause()


    # def displayImage(self, img):
    #     self.scene1.clear()
    #
    #     pixMap = QPixmap(img)
    #     w, h = pixMap.width(), pixMap.height()
    #     self.scene1.addPixmap(pixMap)
    #     self.view1.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
    #     self.scene1.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Scan_dialog()
    w.show()

    #  加载字体
    # QtGui.QFontDatabase.addApplicationFont(":/font/pingfang_sc_cu.ttf")
    # app.setFont(QFont("pingfang_sc_cu"))

    socket_towait = recv_socket()
    j = Jump_to()

    # 连接子线程的信号与进程jump函数连接
    socket_towait.trigger.connect(j.jump)  

    # 开始等待服务器信号的子线程
    socket_towait.start()

    sys.exit(app.exec_())
