from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWebKitWidgets import QWebView, QGraphicsWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtCore import QRectF, QSettings, QDir, QUrl, Qt, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QDockWidget, QDialog, QFileDialog, QMessageBox, QDialogButtonBox
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

##
# The DetachableTabWidget adds additional functionality to Qt's QTabWidget that allows it
# to detach and re-attach tabs.
#
# Additional Features:
#   Detach tabs by
#     dragging the tabs away from the tab bar
#     double clicking the tab
#   Re-attach tabs by
#     closing the detached tab's window
#     double clicking the detached tab's window frame
#
# Modified Features:
#   Re-ordering (moving) tabs by dragging was re-implemented
#

try:
    from PyQt5.QtCore import QString
except ImportError:
    QString = str


class EarthTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setWindowTitle('cesium数字地球')
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.webviewItem = QGraphicsWebView()
        self.webviewItem.settings().setAttribute(
            QWebSettings.WebGLEnabled, True)
        self.webviewItem.settings().setAttribute(
            QWebSettings.AcceleratedCompositingEnabled, True)
        url = "http://localhost:8080/Apps/HelloWorld.html"
        self.webviewItem.load(QUrl(url))
        self.scene.addItem(self.webviewItem)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.view)

    def resizeEvent(self, e):
        print('[cesium]: earth tab widget resized({},{})'.format(
            e.size().width(), e.size().height()))
        self.view.setGeometry(0, 0, e.size().width(),
                              e.size().height())
        self.scene.setSceneRect(0, 0, self.view.viewport().width(),
                                self.view.viewport().height())
        QtWidgets.QTabWidget.resizeEvent(self, e)
