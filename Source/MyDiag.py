# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jsh\Desktop\myDialogUi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_myDialog(object):
    def setupUi(self, myDialog):
        myDialog.setObjectName(_fromUtf8("myDialog"))
        myDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialog.resize(580, 360)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("small-heart.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        myDialog.setWindowIcon(icon)

        self.myBtn = QtGui.QPushButton(myDialog)
        self.myBtn.setGeometry(QtCore.QRect(250, 310, 80, 45))

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("맑은 고딕"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.myBtn.setFont(font)
        self.myBtn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"

                                                
"border-style: outset; \n"
"border-width: 2px; \n"
"border-radius: 15px; \n"
"border-color: black; \n"
"padding: 4px;"))
        self.myBtn.setObjectName(_fromUtf8("myBtn"))

        self.retranslateUi(myDialog)
        QtCore.QMetaObject.connectSlotsByName(myDialog)

    def retranslateUi(self, myDialog):
        myDialog.setWindowTitle(_translate("myDialog", "Drowsiness detection", None))
        self.myBtn.setText(_translate("myDialog", "시작", None))
