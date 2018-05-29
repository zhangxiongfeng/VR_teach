# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("background-image: url(:/img/AR教学视频v1.0/assets/scan_background.jpg);")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setEnabled(True)
        self.widget.setGeometry(QtCore.QRect(750, 230, 420, 430))
        self.widget.setBaseSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        self.widget.setPalette(palette)
        self.widget.setMouseTracking(False)
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

import res_rc
