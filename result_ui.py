# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setStyleSheet("background-image: url(:/img/AR教学视频v1.0/assets/finish_score.png.png);\n"
"background-color:#00b99e;\n"
"")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(870, 430, 171, 141))
        self.label.setStyleSheet("color:#444a49;\n"
"font: 70pt \"Adobe 黑体 Std R\";\n"
"background-color:NONE;")
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(600, 90, 711, 131))
        self.label_5.setStyleSheet("font: 45pt \"Palatino Linotype\";\n"
"color: rgb(255, 255, 255);\n"
"background-color:NONE;")
        self.label_5.setObjectName("label_5")
        self.label.raise_()
        self.label.raise_()
        self.label_5.raise_()
        self.verticalLayout.addWidget(self.widget)
        self.result_info = QtWidgets.QWidget(Dialog)
        self.result_info.setStyleSheet("background-color:white;")
        self.result_info.setObjectName("result_info")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.result_info)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 100)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.cal_icon = QtWidgets.QLabel(self.result_info)
        self.cal_icon.setMinimumSize(QtCore.QSize(54, 54))
        self.cal_icon.setMaximumSize(QtCore.QSize(54, 54))
        self.cal_icon.setStyleSheet("image: url(:/img/AR教学视频v1.0/assets/finish_icon_time.png.png);\n"
"border:NONE;\n"
"")
        self.cal_icon.setText("")
        self.cal_icon.setObjectName("cal_icon")
        self.horizontalLayout_7.addWidget(self.cal_icon)
        self.label_11 = QtWidgets.QLabel(self.result_info)
        self.label_11.setMinimumSize(QtCore.QSize(55, 30))
        self.label_11.setMaximumSize(QtCore.QSize(55, 30))
        self.label_11.setStyleSheet("border:NONE;\n"
"font: 20pt \"Adobe 黑体 Std R\";")
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11, 0, QtCore.Qt.AlignVCenter)
        self.cal_num = QtWidgets.QLabel(self.result_info)
        self.cal_num.setStyleSheet("")
        self.cal_num.setObjectName("cal_num")
        self.horizontalLayout_7.addWidget(self.cal_num, 0, QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, -1, -1, 100)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.cal_icon_2 = QtWidgets.QLabel(self.result_info)
        self.cal_icon_2.setMinimumSize(QtCore.QSize(54, 54))
        self.cal_icon_2.setMaximumSize(QtCore.QSize(54, 54))
        self.cal_icon_2.setStyleSheet("image: url(:/img/AR教学视频v1.0/assets/finish_icon_score.png.png);\n"
"border:NONE;\n"
"")
        self.cal_icon_2.setText("")
        self.cal_icon_2.setObjectName("cal_icon_2")
        self.horizontalLayout_8.addWidget(self.cal_icon_2)
        self.label_12 = QtWidgets.QLabel(self.result_info)
        self.label_12.setMinimumSize(QtCore.QSize(55, 30))
        self.label_12.setMaximumSize(QtCore.QSize(55, 30))
        self.label_12.setStyleSheet("border:NONE;\n"
"font: 20pt \"Adobe 黑体 Std R\";")
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12, 0, QtCore.Qt.AlignVCenter)
        self.cal_num_2 = QtWidgets.QLabel(self.result_info)
        self.cal_num_2.setStyleSheet("")
        self.cal_num_2.setObjectName("cal_num_2")
        self.horizontalLayout_8.addWidget(self.cal_num_2, 0, QtCore.Qt.AlignVCenter)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, -1, -1, 100)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.cal_icon_3 = QtWidgets.QLabel(self.result_info)
        self.cal_icon_3.setMinimumSize(QtCore.QSize(54, 54))
        self.cal_icon_3.setMaximumSize(QtCore.QSize(54, 54))
        self.cal_icon_3.setStyleSheet("image: url(:/img/AR教学视频v1.0/assets/finish_icon_calories.png.png);\n"
"border:NONE;\n"
"")
        self.cal_icon_3.setText("")
        self.cal_icon_3.setObjectName("cal_icon_3")
        self.horizontalLayout_9.addWidget(self.cal_icon_3)
        self.label_13 = QtWidgets.QLabel(self.result_info)
        self.label_13.setMinimumSize(QtCore.QSize(55, 30))
        self.label_13.setMaximumSize(QtCore.QSize(55, 30))
        self.label_13.setStyleSheet("border:NONE;\n"
"font: 20pt \"Adobe 黑体 Std R\";")
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_9.addWidget(self.label_13, 0, QtCore.Qt.AlignVCenter)
        self.cal_num_3 = QtWidgets.QLabel(self.result_info)
        self.cal_num_3.setStyleSheet("")
        self.cal_num_3.setObjectName("cal_num_3")
        self.horizontalLayout_9.addWidget(self.cal_num_3, 0, QtCore.Qt.AlignVCenter)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.horizontalLayout.addLayout(self.horizontalLayout_9)
        self.verticalLayout.addWidget(self.result_info)
        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">100</p></body></html>"))
        self.label_5.setText(_translate("Dialog", "太棒了！恭喜你完成训练~"))
        self.label_11.setText(_translate("Dialog", "<html><head/><body><p>时长</p></body></html>"))
        self.cal_num.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:42pt; color:#444a49;\">18:32</span><span style=\"font: 20pt \"Adobe 黑体 Std R\";\">分</span></p></body></html>"))
        self.label_12.setText(_translate("Dialog", "<html><head/><body><p>得分</p></body></html>"))
        self.cal_num_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:42pt; color:#444a49;\">92</span><span style=\"font: 20pt \"Adobe 黑体 Std R\";\">分</span></p></body></html>"))
        self.label_13.setText(_translate("Dialog", "<html><head/><body><p>消耗</p></body></html>"))
        self.cal_num_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:42pt; color:#444a49;\">333</span><span style=\"font: 20pt \"Adobe 黑体 Std R\";\">千卡</span></p></body></html>"))

import res_rc
