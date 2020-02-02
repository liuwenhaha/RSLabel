from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from .label_dialog import *
from .tool_bar import *
from .label_file import *
from .labelme2COCO import *
from .label_qlist_widget import *
from .escapable_qlist_widget import *
from .utils import struct
from .utils import addActions
from .utils import fmtShortcut
from .utils import newAction
from .utils import newIcon, newImage
from .color_dialog import *
import glob
import shutil
import copy
import functools
import os.path as osp
from PIL.ImageQt import ImageQt
from PIL import Image
import av
from rslabel.gui import qtMouseListener
from rslabel.gui import AHDockWidget
import subprocess
from pathlib import Path
import threading

here = os.path.dirname(os.path.realpath(__file__))


class Decoder(object):
    def __init__(self):
        pass

    def thumbnail(self, videoFile):
        '''
        create a thumbnail from video file
        '''
        container = av.open(videoFile)
        index = 0
        for frame in container.decode(video=0):
            img = frame.to_image()
            index += 1
            if (index == 10):
                qim = ImageQt(img)
                ratio = qim.height() * 1.0 / qim.width()
                pix = QtGui.QPixmap.fromImage(qim)
                pix = pix.scaled(128, 128, Qt.KeepAspectRatio)
                print(type(pix))
                return pix, ratio


class VideoLabel(QtWidgets.QLabel):
    
    prevLabel = None
    labelList = []
    currIndex = -1
    
    def __init__(self, thumbnail, ratio, videoPath, parent=None):
        super(VideoLabel, self).__init__(parent)
        self.thumbnail = thumbnail
        self.ratio = ratio
        # self.setMinimumHeight(129)
        self.width = 160
        self.height = 128
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.videoPath = videoPath
        # self.grabKeyboard()

    def paintEvent(self, event):
        realHeight = int(self.ratio * 128)
        # target = QRect(0, (128 - realHeight) / 2, 128, (128 + realHeight) / 2)
        # src = QRect(0, 0, 128, (128 + realHeight) / 2)
        target = QRect((self.width - 128) / 2, (self.height - realHeight) / 2, 128, realHeight)
        src = QRect(0, 0, 128, realHeight)
        print('* realHeight = ', realHeight)
        painter = QPainter(self)
        
        # color = QColor(0, 155, 0)
        # painter.fillRect(0, 0, 127, 127, color)
        painter.drawPixmap(target, self.thumbnail, src)
        # painter.drawLine(0, 0, 127, 0)
        # painter.drawLine(0, 127, 127, 127)

    def mouseDoubleClickEvent(self, event):
        # 创建播放线程
        vlcThread = VlcThread(self.videoPath)
        # 开启线程
        vlcThread.start()

    def mousePressEvent(self, event):
        onMousePressEvent(self)


class VideoDockWidget(AHDockWidget):
    def __init__(self, name, parent=None):
        super(VideoDockWidget, self).__init__(name, parent)
        self.setMinimumWidth(129)

    def addVideos(self, decoder, videos):
        '''
        video file names
        '''
        self.clear()

        scroller = QScrollArea(self)
        layout = QVBoxLayout()
        scroller.setLayout(layout)
        num = len(videos)
        for index in range(num):
            thumbnail, ratio = decoder.thumbnail(videos[index])
            label = VideoLabel(thumbnail, ratio, videos[index].replace('/', '\\'), self)
            layout.addWidget(label)
            VideoLabel.labelList.append(label)
        layout.addStretch()
        self.setWidget(scroller)

        return

    def clear(self):
        '''
        remove all labels
        '''
        return

    def keyReleaseEvent(self, event):
        labelList = VideoLabel.labelList
        currIndex = VideoLabel.currIndex
        countLabel = len(labelList)
        if labelList and currIndex != -1:
            if event.key() == Qt.Key_Up:
                nextIndex = (currIndex - 1) % countLabel
                onMousePressEvent(labelList[nextIndex])
            elif event.key() == Qt.Key_Down:
                nextIndex = (currIndex + 1) % countLabel
                onMousePressEvent(labelList[nextIndex])
            elif event.key() == Qt.Key_Enter or Qt.Key_Space:
                # 创建播放线程
                vlcThread = VlcThread(labelList[currIndex].videoPath)
                # 开启线程
                vlcThread.start()

class VlcThread(threading.Thread):
    def __init__(self, videoPath):
        threading.Thread.__init__(self)
        self.videoPath = videoPath

    def run(self):
        subprocess.run([str(Path(__file__).parent.joinpath('vlc-3.0.8/vlc.exe')), self.videoPath])


def showMessage(parent, tittle="tittle", message="message"):
    QtWidgets.QMessageBox.information(parent, tittle, message)

def onMousePressEvent(parent):
    if VideoLabel.prevLabel is not None:
        VideoLabel.prevLabel.setStyleSheet("background-color:white")
    parent.setStyleSheet("background-color:orange")
    VideoLabel.prevLabel = parent
    VideoLabel.currIndex = list.index(VideoLabel.labelList, parent)