import sys
import os
import math
import operator
import locale
import traceback
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QDockWidget, QDialog, QFileDialog, QMessageBox, QDialogButtonBox
from PyQt5.QtCore import QSettings, QDir, QUrl, QFileInfo, Qt, pyqtSlot
from .DetachableTabWidget import *


def createTabWidget(parent):
    tabWidget = DetachableTabWidget(parent)
    tabWidget.setWindowTitle('cesium数字地球')
    webview = QWebView()
    url = "http://localhost:8080/Apps/HelloWorld.html"
    webview.load(QUrl(url))
    tabWidget.setLayout(QVBoxLayout())
    tabWidget.layout().addWidget(webview)
    return tabWidget


class cesiumDialog(QDockWidget):
    def __init__(self, iface, parent):
        super(cesiumDialog, self).__init__(parent)
        self.iface = iface
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(QVBoxLayout())
        self.setWindowTitle('cesium数字地球')
        try:
            print("[here is]:", __file__, sys._getframe().f_lineno)
            self.webview = QWebView()
            url = "http://localhost:8080/Apps/HelloWorld.html"
            self.webview.load(QUrl(url))
            self.centralWidget.layout().addWidget(self.webview)
            self.setWidget(self.centralWidget)
        except:
            traceback.print_exc()
