# -*- coding: utf-8 -*-

#******************************************************************************
#
# QMetaTiles
# ---------------------------------------------------------
# Generates tiles (using metatiles) from a QGIS project
#
# Copyright (C) 2015-0219 we-do-IT (info@we-do-it.com)
# Copyright (C) 2012-2014 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************


import os
import configparser

from qgis.PyQt.QtCore import QLocale, QUrl
from qgis.PyQt.QtGui import QPixmap, QTextDocument, QDesktopServices
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog

from .ui.ui_aboutdialogbase import Ui_Dialog

from . import resources_rc


class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.btnHelp = self.buttonBox.button(QDialogButtonBox.Help)

        self.lblLogo.setPixmap(QPixmap(':/icons/qmetatiles.png'))

        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), 'metadata.txt'))
        version = cfg.get('general', 'version')

        self.lblVersion.setText(self.tr('Version: %s') % version)
        doc = QTextDocument()
        doc.setHtml(self.getAboutText())
        self.textBrowser.setDocument(doc)
        self.textBrowser.setOpenExternalLinks(True)

        self.buttonBox.helpRequested.connect(self.openHelp)

    def reject(self):
        QDialog.reject(self)

    def openHelp(self):
        QDesktopServices.openUrl(QUrl('https://bitbucket.org/we-do-it/qgis-latlongo-stage-1/wiki/'))   

    def getAboutText(self):
        return self.tr('<p>Generate tiles(using metatiles) from a QGIS project.</p>'
            '<p>Plugin generates raster tiles (optionally using metatiling) from QGIS project corresponding '
            'to <a '
            'href="http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames">'
            'Slippy Map</a> '
            'specification. Output tiles can be saved in directory or as zip '
            'archive.</p>'
            '<p>Provides a QGIS export for the <a href="http://latlongo.com">LatLonGO®</a> mobile solution.'
            '<p><strong>Developers</strong>: '
            '<a href="http://we-do-it.com">we-do-IT</a><br><br>based on QTiles by <a href="http://nextgis.org">NextGIS</a>, portions of code by '
            'Andrew Naplavkov and Giovanni Allegri.</p>'
            '<p><strong>Homepage</strong>: '
            '<a href="https://bitbucket.org/we-do-it/qgis-latlongo-stage-1">'
            'https://bitbucket.org/we-do-it/qgis-latlongo-stage-1</a></p>'
            '<p>Please report bugs at '
            '<a href="https://bitbucket.org/we-do-it/qgis-latlongo-stage-1/issues">'
            'bugtracker</a></p>'
            )
