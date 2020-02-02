import os
import sys
import traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .cesiumDialog import cesiumDialog, createTabWidget
from .aboutdialog import AboutDialog
from .cesium_utils import *
from . import resources_rc


class cesiumPlugin:
    def __init__(self, iface):
        self.iface = iface
        print("[here is]:", __file__, sys._getframe().f_lineno)
        # start node js process
        startNodejs()

        userPluginPath = './python/plugins/cesium'
        systemPluginPath = './python/plugins/cesium'
        print("[here is]:", __file__, sys._getframe().f_lineno)
        overrideLocale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value('locale/userLocale', '')

        if QFileInfo(userPluginPath).exists():
            translationPath = userPluginPath + '/i18n/cesium_' + localeFullName + '.qm'
        else:
            translationPath = systemPluginPath + '/i18n/cesium_' + localeFullName + '.qm'
        self.localePath = translationPath
        print("[here is]:", __file__, sys._getframe().f_lineno)

        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        print("[here is]:", __file__, sys._getframe().f_lineno)
        self.actionRun = QAction('cesium', self.iface.mainWindow())
        print("[here is]:", __file__, sys._getframe().f_lineno)
        self.iface.registerMainWindowAction(self.actionRun, 'Shift+C')
        self.actionRun.setIcon(QIcon(':/icons/Cesium_Logo_Flat.png'))
        self.actionRun.setWhatsThis('cesium global earth')
        self.actionAbout = QAction(QCoreApplication.translate(
            'cesium', 'About cesium...'), self.iface.mainWindow())
        self.actionAbout.setIcon(QIcon(':/icons/about.png'))
        self.actionAbout.setWhatsThis('About cesium')

        self.iface.addPluginToMenu(QCoreApplication.translate(
            'cesium', 'cesium'), self.actionRun)
        # self.iface.addPluginToMenu(QCoreApplication.translate(
        #    'cesium', 'cesium'), self.actionAbout)
        # self.iface.addToolBarIcon(self.actionRun)
        print("[here is]:", __file__, sys._getframe().f_lineno)
        self.toolbar = QToolBar('cesium')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn = QToolButton()
        btn.setDefaultAction(self.actionRun)
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.addWidget(btn)
        self.iface.addToolbar(self.toolbar)
        print("[here is]:", __file__, sys._getframe().f_lineno)

        try:
            '''
            self.cesiumDialog = cesiumDialog(
                self.iface, self.iface.mainWindow())
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.cesiumDialog)
            '''
            self.cesiumDialog = createTabWidget(self.iface.mainWindow())
            self.tabIndex = self.iface.addTabWidget(self.cesiumDialog)
            self.cesiumDialog.hide()
        except Exception as e:
            print('[cesium]: unhandled exception', e)
            traceback.print_exc()
        self.actionRun.triggered.connect(self.run)
        self.actionAbout.triggered.connect(self.about)

    def unload(self):
        self.iface.unregisterMainWindowAction(self.actionRun)

        self.iface.removeToolBarIcon(self.actionRun)
        self.iface.removePluginMenu(QCoreApplication.translate(
            'cesium', 'cesium'), self.actionRun)
        self.iface.removePluginMenu(QCoreApplication.translate(
            'cesium', 'cesium'), self.actionAbout)

    def run(self):
        if (self.cesiumDialog.isHidden()):
            self.cesiumDialog.show()
            self.tabIndex = self.iface.addTabWidget(self.cesiumDialog)
        else:
            self.iface.removeTabWidget(self.tabIndex)
            self.cesiumDialog.hide()

    def about(self):
        d = AboutDialog()
        d.exec_()
