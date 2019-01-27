# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'amount.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(277, 210)
        self.card_1 = QtWidgets.QPushButton(Dialog)
        self.card_1.setGeometry(QtCore.QRect(60, 100, 75, 23))
        self.card_1.setObjectName("card_1")
        self.card_3 = QtWidgets.QPushButton(Dialog)
        self.card_3.setGeometry(QtCore.QRect(160, 100, 75, 23))
        self.card_3.setObjectName("card_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 40, 171, 31))
        self.label.setObjectName("label")
        self.choice = QtWidgets.QRadioButton(Dialog)
        self.choice.setGeometry(QtCore.QRect(60, 140, 161, 31))
        self.choice.setObjectName("choice")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.card_1.setText(_translate("Dialog", "1"))
        self.card_3.setText(_translate("Dialog", "3"))
        self.label.setText(_translate("Dialog", "Сколько карт в раздаче?"))
        self.choice.setText(_translate("Dialog", "Запомнить мой выбор"))

