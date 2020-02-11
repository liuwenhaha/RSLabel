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
from .ui.ui_tiledialog import Ui_Dialog
from .tilingthread import *
from .utils import newIcon


class QTilesDialog(QDialog, Ui_Dialog):

    def __init__(self, filename, outdir):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(newIcon('tile'))
        self.swne = None
        self.workThread = TilingThread(filename, outdir)
        self.workThread.rangeChanged.connect(self.setProgressRange)
        self.workThread.updateProgress.connect(self.updateProgress)
        self.workThread.processFinished.connect(self.processFinished)
        self.workThread.processInterrupted.connect(self.processInterrupted)
        self.workThread.noSrs.connect(self.noSrs)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.rejected.connect(self.stopProcessing)
        self.workThread.start()

    def noSrs(self):
        mb = QtWidgets.QMessageBox
        msg = '该图像缺少投影信息'
        info = mb.information(self,
                              '失败',
                              msg)
        QDialog.reject(self)

    def setProgressRange(self, message, value):
        self.progressBar.setFormat(message)
        self.progressBar.setRange(0, value)

    def updateProgress(self, n):
        self.progressBar.setValue(n)

    def processInterrupted(self):
        print('[cesium]: cutting tile thread interrupt')

    def processFinished(self):
        print('[cesium]: cutting tile thread finished')
        self.swne = self.workThread.swne
        self.stopProcessing()
        QDialog.accept(self)

    def stopProcessing(self):
        if self.workThread is not None:
            print('[cesium]: cutting tile thread abort')
            self.workThread.stop()
            self.workThread = None
            QDialog.reject(self)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        QDialog.accept(self)
