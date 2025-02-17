# -*- coding: UTF-8 -*-
import urllib.request
import websocket
import simplejson as json
import qrcode
import os
import math
import sys
import time
import threading
import scan_dialog_ui
import player_ui
import wait_select_ui
import result_ui

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer,QCamera,  QCameraImageCapture
from moviepy.editor import VideoFileClip
from PyQt5.QtMultimediaWidgets import QVideoWidget,QCameraViewfinder
from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QPixmap


SERVER_URL = "ws://dev-accwssail.healthmall.cn/server/bodyAnaylzer/data"
MID = "0001"
play_times = 0

class globalData(object):
    def __init__(self):
        # 初始化变量
        self.global_dict = {
            "memberId": "",
            "memberName": "",
            "memHeadImg": "",
            "sectionList": "",
            "courseName": "",
        }

    def set_data(self, data, value):
        if data in self.global_dict.keys():
            self.global_dict[data] = value
        else:
            print("您输入的变量[%s]不存在" % data)

    def get_data(self, data):
        if data in self.global_dict.keys():
            return self.global_dict[data]

        else:
            print("您想获取的变量[%s]不存在" % data)

# 初始界面
class Scan_dialog(QtWidgets.QDialog, scan_dialog_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(Scan_dialog, self).__init__()

        # TODO 初始化个人信息
        data.__init__()

        # 生成二维码
        qrcodeInfo = "https://accwsiot.healthmall.cn/unAppOpen?id=AR" + MID

        self.setupUi(self) 

        self.make_qr(qrcodeInfo)

        # # 更新qrc文件
        # os.system('pyrcc5.exe res.qrc -o res_rc.py')

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
        self.timer_result.stop()
        j.jump("jumpToScan")

# 视频播放
class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)

    def setupVideoUi(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.camera = QCamera(0)
        self.cameraviewfinder = QCameraViewfinder()
        self.cameraviewfinder.setAspectRatioMode(Qt.IgnoreAspectRatio)

        self.cameramode = self.camera.CaptureMode(2)
        self.cameraimgcap = QCameraImageCapture(self.camera)

        self.videoWidget = QVideoWidget()

        self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.camera.setViewfinder(self.cameraviewfinder)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self, fileNameList):
        self.fileNameList = fileNameList
        self.play_next()

    def play_next(self):
        global play_times

        if play_times == len(self.fileNameList):
                self.timer_play.stop()
                return

        single_file = self.fileNameList[play_times]
        try:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(single_file)))
        except Exception:
            print("配置视频播放出错")
            print(Exception)

        #播放视频
        self.mediaPlayer.play()

        # 开启倒计时,进行连续播放
        self.single_time = math.ceil(self.getDuration(single_file))

        self.timer_play = QtCore.QTimer()
        self.timer_play.timeout.connect(self.play_next)

        # 定时器以毫秒作为单位
        self.timer_play.start(self.single_time * 1000)

        play_times = play_times + 1

    def camera_start(self):
        # 开启摄像头
        # self.cameraviewfinder.resize(640, 480)
        self.camera.start()

    # 获取视频时长(单位为秒)
    def getDuration(self, fileName):
        total_times = 0

        if type(fileName) != list:
            clip = VideoFileClip(fileName)
            single_time = clip.duration
            clip.reader.close()
            clip.audio.reader.close_proc()
            return single_time

        for f in fileName:
            clip = VideoFileClip(f)
            times = clip.duration
            total_times = total_times + times
            clip.reader.close()
            clip.audio.reader.close_proc()
        return total_times

    def pause(self):
       self.mediaPlayer.pause()

# 创建跳转对象
class Jump_to(VideoWindow):
    def __init__(self):
        super(Jump_to, self).__init__()
        self.duration = 0
        self.memberId = 0
        self.memHeadImg = ""
        self.memberName = ""
        self.courseName = ""
        self.sectionList = ""
        self.start_time = 0
        self.fileNameList = []

    def jump(self, command):
        global play_times

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

            # 重置播放次数
            play_times = 0

            # 判断是否在视频播放阶段
            try:
                self.pause()
                self.timer_play.stop()

            except Exception:
                print(Exception)

            w.showFullScreen()

        elif command == "jumpToWait":
            # 关闭上层窗口
            w.setHidden(True)

            self.w2 = Wait_ui()
            self.w2.showFullScreen()

        elif command == "jumpToPlay":
            self.start_time = time.time()
            print("开始时间[%f]" % self.start_time)

            self.jump_to_play()

        elif command == "jumpToResult":
            # 重置播放次数
            play_times = 0

            self.jump_to_result()

    def jump_to_result(self):
         # 关闭上层窗口
        self.w3.setHidden(True)

        # TODO 完善下面这句代码
        self.pause()

        self.w4 = Result_ui()
        self.w4.showFullScreen()

    def jump_to_play(self):
        self.wait_text = "已选课程，请稍等"
        self.w2.label_2.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; color:#444a49;letter-spacing:6px\">"+self.wait_text+"</span></p></body></html>")

        # 等待线程完成发送信号,防止UI线程阻塞
        self.change_thread = change_text()
        self.change_thread.start()
        self.change_thread.change_trigger.connect(self.display_player)

        self.w3 = Player_ui()

    def display_player(self):
        # 获取全局变量
        self.courseName = data.get_data("courseName")
        self.memberName = data.get_data("memberName")

        # 设置学生头像
        self.w3.user_icon.setStyleSheet("border-image: url(:/img/AR教学视频v1.0/res/user_icon.selfpg);\n"
    "border:NONE\n")

        # TODO 需要老师名称和头像地址
        self.w3.tech_name.setText("<html><head/><body><p><span style=\" font-size:26pt; color:#ffffff;\">陈老师</span></p></body></html>")
        self.w3.course_name.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#fff;\">"+self.courseName+"</span></p></body></html>")
        self.w3.cal_num.setText("<html><head/><body><p><span style=\" font-size:42pt; color:#fff;\">320</span><span style=\" font-size:22pt; color:#939a99;\">千卡</span></p></body></html>")
        self.w3.user_name.setText( "<html><head/><body><p><span style=\" font-family:\'PingFang SC\'; font-size:26pt; color:#ffffff;\">"+self.memberName+"</span></p></body></html>")
        self.w3.goal_num.setText("<html><head/><body><p><span style=\" font-size:42pt; color:#fff;\">89</span><span style=\" font-size:22pt; color:#939a99;\">/100分</span></p></body></html>")

        # TODO 加上视频播放功能
        self.fileNameList = [os.getcwd()+'\\teacher_1.mp4', ]

        # 创建播放器和摄像头UI
        VideoWindow.setupVideoUi(self)
        # 开启摄像头
        self.camera_start()

        # 初始化播放时长,向上取整
        self.duration = math.ceil(self.getDuration(self.fileNameList))
        timer_text = ("%02d:%02d" % (self.duration / 60, (self.duration % 60)))
        self.w3.time.setText("<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">" + str(timer_text) + "</span></p></body></html>")

        self.w3.horizontalLayout_2.addWidget(self.videoWidget)
        self.w3.horizontalLayout_2.addWidget(self.cameraviewfinder)

        # 设置居中平分
        self.w3.horizontalLayout_2.setStretch(0, 1)
        self.w3.horizontalLayout_2.setStretch(1, 1)

        # 初始化定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer_display)

        # 关闭上层窗口
        self.w2.setHidden(True)
        self.w3.showFullScreen()

        # 开始播放,开启倒计时
        self.play(self.fileNameList)
        self.timer.start(1000)

        # 计算播放时间
        finish_time = time.time() - j.start_time
        print("finish_time:%f" % finish_time)

    def update_timer_display(self):
        self.duration = self.duration - 1

        timer_text = ("%02d:%02d" % (self.duration / 60, (self.duration % 60)))
        self.w3.time.setText("<html><head/><body><p><span style=\" font-size:24pt; color:#ffffff;\">" + str(timer_text) + "</span></p></body></html>")

        # 播放结束后自动跳转
        if self.duration == 0:
            # 关闭定时器
            self.timer.stop()
            if self.w3.isVisible():
                self.jump_to_result()

class change_text(QThread, VideoWindow):
    change_trigger = pyqtSignal()
    def __init__(self):
        super(change_text, self).__init__()

    # 更改等待界面文字新建线程
    def run(self):
        print("接收时间[%f]" % (time.time() - j.start_time))

        # 保存学生头像，覆盖默认图片
        # self.memHeadImg = data.get_data("memHeadImg")
        # path = os.getcwd() + '/AR教学视频v1.0/res/user_icon.jpg'
        # urllib.request.urlretrieve(self.memHeadImg, path)

        self.change_trigger.emit()

# 创建服务器连接
class recv_socket(QThread):
    # 声明信号，发送信号时传入list
    trigger = pyqtSignal(str)

    def __init__(self):
        super(recv_socket, self).__init__()
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
        # json转化为dict
        dict_message = json.loads(message_server)

        message = dict_message["message"]

        if message == "register success":
            # TODO 需要一些保护机制
            pass

        elif message == "register failed":
            print("设备注册失败,尝试重新发送注册信息")
            print(self.ws)
            self.on_open(self, self.ws)

        elif "failed" in message:
            message_split = message.split()
            print("[%s]出错:[%s]" % (message_split[0], message_split[1]))

        # 解锁界面
        elif message == "unlock":
            # 设置全局变量
            data.set_data("memberId", dict_message["memberId"])
            data.set_data("memberName", dict_message["memberName"])
            data.set_data("memHeadImg", dict_message["memHeadImg"])

            # 页面信号
            self.trigger.emit("jumpToWait")

            # 以json形式返回message
            send_message = {"message": "unlock ok"}
            ws.send(json.dumps(send_message))
        
        elif message == "lock":
            # 发送跳转信号
            self.trigger.emit("jumpToScan")

            send_message = {"message": "lock ok"}

            ws.send(json.dumps(send_message))

        elif message == "executeList":

            data.set_data("courseName", dict_message["courseName"])
            data.set_data("sectionList", dict_message["sectionList"])

            self.trigger.emit("jumpToPlay")

            # 以json形式返回message
            send_message = {"message": "executeList ok"}
            ws.send(json.dumps(send_message))

        elif message == "closure":
            print("结束视频")

            # 发送跳转信号
            self.trigger.emit("jumpToResult")
            # 以json形式返回message
            send_message = {"message": "closure ok"}

            ws.send(json.dumps(send_message))

    def on_error(self, ws, error):
        print(error)

    def on_open(self, ws):
        # 发送机器唯一标识码
        ws.send("{\"message\":\"register\",\"deviceID\":\"AR000001\"}")

    def on_close(self, ws):
        print("close:")
        print(ws)
        # 尝试重新连接
        self.run()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # 初始化变量
    data = globalData()

    w = Scan_dialog()
    w.showFullScreen()

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
