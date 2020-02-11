# -*- coding: utf-8 -*-

# ******************************************************************************
#
# QMetaTiles
# ---------------------------------------------------------
# Generates tiles (using metatiles) from a QGIS project
#
# Copyright (C) 2015-2019 we-do-IT (info@we-do-it.com)
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
# ******************************************************************************

import math
import time
from PyQt5.QtCore import QThread, QMutex, pyqtSignal
from .gdal2tiles import *


class TilingThread(QThread):
    rangeChanged = pyqtSignal(str, int)
    updateProgress = pyqtSignal(int)
    processFinished = pyqtSignal()
    processInterrupted = pyqtSignal()
    noSrs = pyqtSignal()

    def __init__(self, filename, outdir):
        QThread.__init__(self, QThread.currentThread())
        self.mutex = QMutex()
        self.stopMe = 0
        self.swne = None
        self.interrupted = False
        self.filename = filename
        self.outdir = outdir
        self.swne = None

    def run(self):
        self.mutex.lock()
        self.stopMe = 0
        self.mutex.unlock()
        #  generate a list of tiles.
        self.rangeChanged.emit(self.tr('切片...'), 100)
        try:
            self.swne = generate_tiles(
                self, self.filename, self.outdir, resume=True)
        except:
            self.noSrs.emit()
        if(self.swne is None):
            self.processInterrupted.emit()
        else:
            self.processFinished.emit()

    def stop(self):
        self.mutex.lock()
        self.stopMe = 1
        self.mutex.unlock()
        QThread.wait(self)
