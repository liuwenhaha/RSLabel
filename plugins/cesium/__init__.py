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
from PyQt5.uic import *
from PyQt5.uic import properties, uiparser, Compiler
from PyQt5.uic.objcreator import widgetPluginPath
from PyQt5.uic.Compiler import indenter, compiler
import warnings
print("[cesium]: __init__")


__appname__ = 'cesium'


def name():
    return "cesium plugin"


def classFactory(iface):
    from .cesium import cesiumPlugin
    return cesiumPlugin(iface)


def description():
    return "cesium 3d earth"


def version():
    return "Version 0.1"
