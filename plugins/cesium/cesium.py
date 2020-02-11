import os
import sys
import traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from .cesiumDialog import cesiumDialog, createTabWidget, createEarthWidget
from .cesium_utils import *
from . import resources_rc
from .tileDialog import *
from .gdal2tiles import *


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
        self.action2Earth = QAction('On Earth', self.iface.mainWindow())
        self.action2Earth.setIcon(QIcon(':/icons/toEarth.png'))
        self.action2Earth.setWhatsThis('add layer to cesium global earth')
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
        btn0 = QToolButton()
        btn0.setDefaultAction(self.actionRun)
        btn0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.addWidget(btn0)
        btn1 = QToolButton()
        btn1.setDefaultAction(self.action2Earth)
        btn1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.addWidget(btn1)
        self.iface.addToolbar(self.toolbar)
        print("[here is]:", __file__, sys._getframe().f_lineno)

        try:
            '''
            self.cesiumDialog = cesiumDialog(
                self.iface, self.iface.mainWindow())
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.cesiumDialog)
            '''
            self.cesiumDialog, self.webview = createTabWidget(
                self.iface.mainWindow(), False)
            self.tabIndex = self.iface.addTabWidget(self.cesiumDialog)
            self.cesiumDialog.hide()
        except Exception as e:
            print('[cesium]: unhandled exception', e)
            traceback.print_exc()
        self.actionRun.triggered.connect(self.run)
        self.action2Earth.triggered.connect(self.image2Earth)
        self.actionAbout.triggered.connect(self.about)

    def progressCB(self, n):
        self.iface.setProgress(n)
        QCoreApplication.processEvents()

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

    def image2Earth(self):
        '''
        tiling the image, add it as an imagery provider
        '''
        currentImg = self.iface.getCurrentFile()
        appdata = os.getenv("APPDATA")
        p, fn = os.path.split(currentImg)
        outdir = os.path.join(appdata, 'rslabel/cache', fn)
        d = QTilesDialog(currentImg, outdir)
        d.show()
        d.exec_()
        swne = d.swne
        if(swne is not None):
            templateContent = "var layers = viewer.scene.imageryLayers;"\
                "var tms = new Cesium.UrlTemplateImageryProvider({{"\
                "url: \"../localfile/{0}/{{z}}/{{x}}/{{reverseY}}.png\","\
                "maximumLevel: 17,"\
                "tileWidth: 256,"\
                "tileHeight: 256"\
                "}});"\
                "layers.addImageryProvider(tms);"\
                "viewer.camera.flyTo({{"\
                "destination: Cesium.Cartesian3.fromDegrees({1}, {2}, 7500.0)"\
                "}});"
            x = float(swne[0] + swne[2]) / 2.0
            y = float(swne[1] + swne[3]) / 2.0
            self.iface.setCurrentTabIndex(self.tabIndex)
            content = templateContent.format(fn, y, x)
            self.webview.page().mainFrame().evaluateJavaScript(content)

        '''
        from optparse import OptionParser, OptionGroup
        currentImg = self.iface.getCurrentFile()
        if (currentImg.strip() != ''):
            print('[cesium]: get the current image', currentImg)
            self.tmp_dir = tempfile.mkdtemp()
            p, fn = os.path.split(currentImg)
            fn, ext = os.path.splitext(fn)
            print('[cesium]:', fn)
            print('[cesium]: temp dir is ', self.tmp_dir)
            appdata = os.getenv("APPDATA")
            print("[cesium]: app data is ", appdata)
            outdir = os.path.join(appdata, 'rslabel/cache', fn)
            tileMap = True
            try:
                swne = generate_tiles(currentImg,
                                      outdir,
                                      callback=self.progressCB,
                                      resume=True)
                print('[cesium]: image scope: ', swne[0:])
            except Exception as e:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(
                    self.iface.mainWindow(), '提示', '<p><b>%s</b></p>%s' % ('提示', '该影像缺少地理信息'))
                tileMap = False
            if (tileMap):
                templateContent = "var layers = viewer.scene.imageryLayers;"\
                    "var tms = new Cesium.UrlTemplateImageryProvider({{"\
                    "url: \"../localfile/{0}/{{z}}/{{x}}/{{reverseY}}.png\","\
                    "maximumLevel: 17,"\
                    "tileWidth: 256,"\
                    "tileHeight: 256"\
                    "}});"\
                    "layers.addImageryProvider(tms);"\
                    "viewer.camera.flyTo({{"\
                    "destination: Cesium.Cartesian3.fromDegrees({1}, {2}, 150.0)"\
                    "}});"
                x = float(swne[0] + swne[2]) / 2.0
                y = float(swne[1] + swne[3]) / 2.0
                self.iface.setCurrentTabIndex(self.tabIndex)
                content = templateContent.format(fn, y, x)
                self.webview.page().mainFrame().evaluateJavaScript(content)
        '''

    def about(self):
        d = AboutDialog()
        d.exec_()
