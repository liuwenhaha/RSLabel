import sys
import os
import math
import operator
import locale
import traceback
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebInspector, QWebView, QGraphicsWebView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QSplitter, QWidget, QDockWidget, QDialog, QFileDialog, QMessageBox, QDialogButtonBox
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QRectF, QSettings, QDir, QUrl, QFileInfo, Qt, pyqtSlot
#from PyQt5.QtWebEngineWidgets import *
from .EarthTabWidget import *


def createEarthWidget(parent):
    earth = EarthTabWidget(parent)
    return earth, earth.webviewItem


def createTabWidget(parent, inspector=False):
    tabWidget = QtWidgets.QTabWidget(parent)
    tabWidget.setWindowTitle('cesium数字地球')
    tabWidget.setLayout(QVBoxLayout())
    webview = QWebView()  # QWebEngineView()
    webview.settings().setAttribute(
        QWebSettings.WebGLEnabled, True)
    webview.settings().setAttribute(
        QWebSettings.AcceleratedCompositingEnabled, True)
    url = "http://localhost:8080/Apps/HelloWorld.html"
    webview.load(QUrl(url))
    webview.settings().setAttribute(
        QWebSettings.DeveloperExtrasEnabled, True)
    if inspector:
        inspector = QWebInspector()
        inspector.setPage(webview.page())
        splitter = QSplitter(parent)
        splitter.addWidget(webview)
        splitter.addWidget(inspector)
        tabWidget.layout().addWidget(splitter)
    else:
        tabWidget.layout().addWidget(webview)

    return tabWidget, webview


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

    def evalJavascript(self, content):
        self.webview.page().mainFrame().evaluateJavaScript(content)
