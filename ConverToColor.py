#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 12:53 2018/8/3

@author:    Liu Jinbao
@mail:      liu.jinbao@outlook.com
@project:   ReadImag
@IDE:       PyCharm
"""

import cv2 as cv
from matplotlib import pyplot as plt
from PyQt5 import QtWidgets as QW

import sys
r"""
sys.path.insert(0, "E:\Coding\Python\ImportToUse")
from BetterQWidgets import BetterQLabel, BetterButton, QPlot


class TheWindow(QW.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cenWidget = QW.QWidget()
        self.setCentralWidget(self.cenWidget)
        self._image = QPlot(figsize=(9, 6))
        self.axes = self._image.add_subplot(111)
        self.axes

        _layout = QW.QVBoxLayout()
        _layout.addWidget(self._image)
        self.cenWidget.setLayout(_layout)

    # def imshow(self, im_data):
    #     self.


if __name__ == '__main__':
    if not QW.QApplication.instance():
        app = QW.QApplication(sys.argv)
    else:
        app = QW.QApplication.instance()
    app.setStyle(QW.QStyleFactory.create("Fusion"))
    window = TheWindow()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
"""

im_gray = cv.imread(r"N:\JPG\DSC_0268.JPG", cv.IMREAD_GRAYSCALE)


# M = cv.getRotationMatrix2D((2000, 2000), 40, 1.0)
# im_rotated = cv.warpAffine(im_gray, M, (im_gray.shape[0], im_gray.shape[1]))


def rotate_img(_im, angle):
    M = cv.getRotationMatrix2D((2000, 2000), angle, 1.0)
    return cv.warpAffine(_im, M, (_im.shape[0], _im.shape[1]))


def show_gray_image(_im_gray):
    im_color_BGR = cv.applyColorMap(_im_gray, cv.COLORMAP_JET)
    # matplotlib use RGB, OpenCV use BGR.
    im_color_RGB = cv.cvtColor(im_color_BGR, cv.COLOR_BGR2RGB)
    # fig = plt.figure()
    # axes = fig.add_subplot(111)
    # plt.imshow(im_color_RGB, vmin=0, vmax=120)
    plt.imshow(_im_gray, vmin=0, vmax=120)

show_gray_image(im_gray)
show_gray_image(rotate_img(im_gray, 15))

# fig = plt.figure()
# axes = fig.add_subplot(111)
# im = axes.imshow(im_gray)
# axes.imshow(rotate_img(im_gray, 90))
# axes.get
# cv2.imshow('image', rotated90)
# cv2.resizeWindow('image', 800, 600)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
r"""
"""
