# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/textdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TextDialog(object):
    def setupUi(self, TextDialog):
        TextDialog.setObjectName("TextDialog")
        TextDialog.resize(507, 653)
        self.verticalLayout = QtWidgets.QVBoxLayout(TextDialog)
        self.verticalLayout.setContentsMargins(3, 5, 3, 5)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(TextDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.designLbl = QtWidgets.QLineEdit(TextDialog)
        self.designLbl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.designLbl.setReadOnly(True)
        self.designLbl.setObjectName("designLbl")
        self.horizontalLayout_3.addWidget(self.designLbl)
        self.designBtn = QtWidgets.QToolButton(TextDialog)
        self.designBtn.setObjectName("designBtn")
        self.horizontalLayout_3.addWidget(self.designBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.searchOptionLayout = QtWidgets.QHBoxLayout()
        self.searchOptionLayout.setSpacing(0)
        self.searchOptionLayout.setObjectName("searchOptionLayout")
        self.followEdit = QtWidgets.QLineEdit(TextDialog)
        self.followEdit.setObjectName("followEdit")
        self.searchOptionLayout.addWidget(self.followEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.searchOptionLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.searchOptionLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(TextDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.dlall = QtWidgets.QPushButton(TextDialog)
        self.dlall.setObjectName("dlall")
        self.horizontalLayout_5.addWidget(self.dlall)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.imgList = QtWidgets.QListWidget(TextDialog)
        self.imgList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imgList.setAutoScroll(False)
        self.imgList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.imgList.setObjectName("imgList")
        self.verticalLayout.addWidget(self.imgList)
        self.line = QtWidgets.QFrame(TextDialog)
        self.line.setLineWidth(5)
        self.line.setMidLineWidth(7)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cancelBtn = QtWidgets.QPushButton(TextDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.startBtn = QtWidgets.QPushButton(TextDialog)
        self.startBtn.setDefault(True)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout.addWidget(self.startBtn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TextDialog)
        QtCore.QMetaObject.connectSlotsByName(TextDialog)

    def retranslateUi(self, TextDialog):
        _translate = QtCore.QCoreApplication.translate
        TextDialog.setWindowTitle(_translate("TextDialog", "Text Setting"))
        self.label_2.setText(_translate("TextDialog", "Book Design: "))
        self.designBtn.setText(_translate("TextDialog", "..."))
        self.followEdit.setPlaceholderText(_translate("TextDialog", "Following text to search with"))
        self.label.setText(_translate("TextDialog", "Images to embed in your book"))
        self.dlall.setText(_translate("TextDialog", "Download All"))
        self.cancelBtn.setText(_translate("TextDialog", "Stop"))
        self.startBtn.setText(_translate("TextDialog", "Start"))

