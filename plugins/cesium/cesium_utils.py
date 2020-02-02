import os
import subprocess
from PyQt5 import QtCore


def getMapLayers():
    layerMap = QgsProject.instance().mapLayers()
    layers = dict()
    for name, layer in layerMap.items():
        if layer.type() == QgsMapLayer.VectorLayer:
            if layer.id() not in layers.keys():
                layers[layer.id()] = layer.name()
        if layer.type() == QgsMapLayer.RasterLayer and layer.providerType() == 'gdal':
            if layer.id() not in layers.keys():
                layers[layer.id()] = layer.name()
    return layers


def getLayerById(layerId):
    layerMap = QgsProject.instance().mapLayers()
    for name, layer in layerMap.items():
        if layer.id() == layerId:
            if layer.isValid():
                return layer
            else:
                return None


def getLayerGroup(relations, layerId):
    group = None

    for item in relations:
        group = unicode(item[0])
        for lid in item[1]:
            if unicode(lid) == unicode(layerId):
                return group

    return group


def startNodejs():
    cmd = './Python/plugins/cesium/nodejs/node.exe'
    arg = './python/plugins/cesium/Cesium-1.65/server.js'
    args = [arg]
    try:
        my_process = QtCore.QProcess()
        my_process.setProgram(cmd)
        my_process.setArguments(args)
        my_process.startDetached()
    except Exception as e:
        print('[cesium]: unhandled exception', e)
        traceback.print_exc()
    '''
    cmd_with_arg = cmd + ' ' + arg
    res = subprocess.run(cmd_with_arg, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = subprocess.Popen(
        cmd_with_arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    '''
