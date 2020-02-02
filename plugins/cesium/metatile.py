# -*- coding: utf-8 -*-

#******************************************************************************
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
#******************************************************************************

import os
from qgis.core import QgsRectangle
from qgis.PyQt.QtGui import QImage
#from qgis.PyQt.QtCore import *
from .tile import Tile
#import pydevd; pydevd.settrace(port=5678)

class Metatile:
    """
        A metatile is a Square or Rectangular group of tiles. It contains tiles for only one zoom level. It contains
        functions to generate a single overall image and functions to slice it up into smaller tiles again.
    """
    def __init__(self, extents, zoom, buffer, parent):
        self.extents = extents
        self.zoom = zoom
        self.buffer = buffer
        self.size = {'rows': (extents[1] - extents[0]) + 1, 'cols': (extents[3] - extents[2]) + 1}
        self.parent = parent
        #  set the metatile width and height in pixels, based on the number and size of tiles.
        self.width = parent.tile_width * self.size['cols']
        self.height = parent.tile_height * self.size['rows']

    def rectangle(self):
        """
        Generate a rectangle that spans this metatile (including the any buffer applied in tileset.py)
        """
        corner_1 = Tile(self.extents[2], self.extents[0], self.zoom ).toPoint()
        corner_2 = Tile(self.extents[3] + 1, self.extents[1] + 1, self.zoom).toPoint()
        return QgsRectangle(corner_1, corner_2)

    def slice(self):
        """
        Write a series of tiles contained within this metatile.
        """
        #  open the metatile
        with open(self.full_path(),'rb') as f:
            #  load the metatile into a QImage
            meta_img = QImage()
            meta_img.loadFromData(f.read())
            #  get the tile range within this metatile (filtering outside tiles if buffered)
            if self.buffer:
                x_min = 1
                y_min = 1
                x_max = self.size['cols'] - 1
                y_max = self.size['rows'] - 1
            else:
                x_min = 0
                y_min = 0
                x_max = self.size['cols']
                y_max = self.size['rows']
            #  loop through the tiles in the metatile and crop the metatile to the tile.
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    #  get the top-left location (in pixels) of the tile to be extracted from the metatile.
                    #  crop the loaded metatile to the tile
                    new_img = meta_img.copy(x * self.parent.tile_width, y * self.parent.tile_height, self.parent.tile_width, self.parent.tile_height)
                    #  get the tile number (x and y)
                    tile_x = self.extents[2] + x
                    tile_y = self.extents[0] + y
                    #  create a Tile instance
                    tile = Tile(tile_x, tile_y ,self.zoom)
                    #  use the selected writer to write the file
                    self.parent.writer.writeTile(tile, new_img, self.parent.format, self.parent.quality)
                    #  destroy the tile in memory - just in case.
                    del new_img
            #  destroy the metatile just in case.
            del meta_img

    def write_metatile(self, image, format, quality):
        """
        Write the image to file(called from tileset).
        """
        image.save(self.full_path(), format, quality)

    def full_path(self):
        """
        Return the absolute path of this metatile.
        """
        return os.path.join(self.parent.metatiles_path, self.file_name())

    def file_name(self):
        """
        Generate a filename for this metatile. This could be used to slice using another application, as it contains zoom and extents.
        """
        return '{0}_&&_{1}_{2}_&&_{3}_{4}.{5}'.format(self.zoom, self.extents[2], self.extents[0], self.extents[3], self.extents[1], self.parent.format.lower())
