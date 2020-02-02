# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\cesium.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CesiumDialog(object):
    def setupUi(self, CesiumDialog):
        CesiumDialog.setObjectName("CesiumDialog")
        CesiumDialog.resize(709, 548)
        self.verticalLayout = QtWidgets.QVBoxLayout(CesiumDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.centralWidget = QtWidgets.QWidget(CesiumDialog)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout.addWidget(self.centralWidget)

        self.retranslateUi(CesiumDialog)
        QtCore.QMetaObject.connectSlotsByName(CesiumDialog)

    def retranslateUi(self, CesiumDialog):
        _translate = QtCore.QCoreApplication.translate
        CesiumDialog.setWindowTitle(_translate("CesiumDialog", "cesium3D"))

