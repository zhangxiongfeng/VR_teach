# PyQt5 Video player
# !/usr/bin/env python
from PyQt5 import  QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl,QRectF
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer,QCamera,  QCameraImageCapture

from PyQt5.QtMultimediaWidgets import QVideoWidget,QCameraViewfinder
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction,QGraphicsScene,QGraphicsView
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QImage,QPixmap
import sys
import cv2,time


class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.camera = QCamera(0)
        self.cameraviewfinder = QCameraViewfinder()
        self.cameramode = self.camera.CaptureMode(2)
        self.cameraimgcap = QCameraImageCapture(self.camera)

        videoWidget = QVideoWidget()
        self.imageView = QLabel("add a image file")
        self.imageView.setAlignment(Qt.AlignCenter)
        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)

        self.scene1 = QGraphicsScene()
        self.view1 = QGraphicsView(self.scene1)


        # Create new action


        # Create exit action




        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)



        # Create layouts to place inside widget
        # controlLayout = QHBoxLayout()
        # controlLayout.setContentsMargins(0, 0, 0, 0)
        # controlLayout.addWidget(self.playButton)
        # controlLayout.addWidget(self.positionSlider)

        videolayout = QVBoxLayout()
        videolayout.addWidget(videoWidget)

        # videolayout.addLayout(controlLayout)
        # Set widget to contain window contents

        layout = QHBoxLayout()
        layout.addLayout(videolayout)
        layout.addWidget(self.cameraviewfinder)
        # layout.addWidget(self.view1)
        wid.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.cameraviewfinder.show()
        self.camera.setViewfinder(self.cameraviewfinder)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        self.showFullScreen()

        fileName = 'D:\\桌面\\some.mp4'

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        self.cameraviewfinder.resize(640, 480)
        self.camera.start()
        self.mediaPlayer.play()

        camera_capture = cv2.VideoCapture(0)

        while True:
            ret, camera_frame = camera_capture.read()
            if ret:
                self.displayImage(camera_frame)
            else:
                break
        camera_capture.release()
        cv2.destroyAllWindows()


    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def displayImage(self, img):
        self.scene1.clear()
        pixMap = QPixmap(img)
        w, h = pixMap.width(), pixMap.height()
        self.scene1.addPixmap(pixMap)
        self.view1.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        self.scene1.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.show()
    player.play()
    sys.exit(app.exec_())
