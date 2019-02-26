#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15:05 2018/7/28

@author:    Liu Jinbao
@mail:      liu.jinbao@outlook.com
@project:   ReadImg
@IDE:       PyCharm
"""
import sys
import math
import cv2
from PIL import Image
from PIL.ExifTags import TAGS
from PyQt5 import QtWidgets as QW
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from BetterQWidgets import QPlot, ReadFileQWidget


class ImagShow(QPlot):

    def __init__(self, parent=None):
        super().__init__(parent, figsize=(9, 9))
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.figure.tight_layout()
        self.set_focus()

    def imshow(self, im):
        self.axes.cla()
        self.axes.imshow(im)
        self.canvas.draw()

    def set_focus(self):
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()


class TheReadFileQWidget(ReadFileQWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _browse_callback(self):
        _path = QW.QFileDialog.getOpenFileName(caption='Open File',
                                               filter="imag file (*.jpg)")[0]
        self.path = _path
        self._entry.setText(_path)


class TheWindow(QW.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cenWidget = QW.QWidget()
        self._read_file = TheReadFileQWidget()
        self._imag_show = ImagShow()
        self._exif_table = QW.QTableWidget()
        self._exif_table.setColumnCount(2)
        self._exif_table.setRowCount(7)
        self.setCentralWidget(self.cenWidget)
        self.setWindowIcon(QIcon('matplotlib_large.png'))
        self.setWindowTitle('Read image and calculate the angle arc swept. Code by Liu Jinbao')
        self._set_layout()
        self._set_connect()

        self.init_marks()
        self.hide_marks()
        self._imag_show.set_focus()

    def get_exif(self, file_path):
        image = Image.open(file_path)
        exif = image._getexif()

        exif_dict = dict()
        for tag, value in exif.items():
            key = TAGS.get(tag)
            if key == 'FNumber':
                exif_dict[key] = 'f/{F:.1f}'.format(F=value[0] / value[1])
            elif key == 'ExposureTime':
                exif_dict[key] = '{t:.1f} ms'.format(t=value[0] / value[1] * 1e3)
            elif key == 'FocalLength':
                exif_dict[key] = '{fo:.0f} mm'.format(fo=value[0] / value[1])
            elif key == 'ISOSpeedRatings':
                exif_dict[key] = 'ISO-{iso:.0f}'.format(iso=value)
            elif key in ['Make', 'Model', 'DateTime']:
                exif_dict[key] = value
            else:
                continue
        return exif_dict

    def init_marks(self):
        self.A_mark, = self._imag_show.axes.plot(0, 0, marker='X', markersize=10, alpha=0.5)
        self.B_mark, = self._imag_show.axes.plot(0, 0, marker='X', markersize=10, alpha=0.5)
        self.C_mark, = self._imag_show.axes.plot(0, 0, marker='X', markersize=10, alpha=0.5)
        self.O_mark, = self._imag_show.axes.plot(0, 0, marker='X', markersize=10, alpha=0.5)
        self.A_sign = self._imag_show.axes.text(0, 0, 'A')
        self.B_sign = self._imag_show.axes.text(0, 0, 'B')
        self.C_sign = self._imag_show.axes.text(0, 0, 'C')
        self.O_sign = self._imag_show.axes.text(0, 0, 'O')
        for _ in [self.A_sign, self.B_sign, self.C_sign, self.O_sign]:
            _.set_size(18)
            _.set_visible(False)
            _.set_color('white')
        self.AO_line, = self._imag_show.axes.plot([0, 0], [0, 0], linestyle='--')
        self.BO_line, = self._imag_show.axes.plot([0, 0], [0, 0], linestyle='--')

    def hide_marks(self):
        self.A_mark.set_visible(False)
        self.B_mark.set_visible(False)
        self.C_mark.set_visible(False)
        self.O_mark.set_visible(False)

    def set_A_mark(self, x, y):
        self.A_mark.set_visible(True)
        self.A_mark.set_xdata(x)
        self.A_mark.set_ydata(y)
        self.A_sign.set_x(x)
        self.A_sign.set_y(y)
        self.A_sign.set_visible(True)
        self._imag_show.canvas.draw()

    def set_B_mark(self, x, y):
        self.B_mark.set_visible(True)
        self.B_mark.set_xdata(x)
        self.B_mark.set_ydata(y)
        self.B_sign.set_x(x)
        self.B_sign.set_y(y)
        self.B_sign.set_visible(True)
        self._imag_show.canvas.draw()

    def set_C_mark(self, x, y):
        self.C_mark.set_visible(True)
        self.C_mark.set_xdata(x)
        self.C_mark.set_ydata(y)
        self.C_sign.set_x(x)
        self.C_sign.set_y(y)
        self.C_sign.set_visible(True)
        self._imag_show.canvas.draw()

    def set_O_mark(self):
        if self.A_mark.get_visible() is False:
            return None
        if self.B_mark.get_visible() is False:
            return None
        if self.C_mark.get_visible() is False:
            return None
        x1 = self.A_mark.get_xdata()
        x2 = self.B_mark.get_xdata()
        x3 = self.C_mark.get_xdata()
        y1 = self.A_mark.get_ydata()
        y2 = self.B_mark.get_ydata()
        y3 = self.C_mark.get_ydata()
        A1 = 2 * (x2 - x1)
        B1 = 2 * (y2 - y1)
        C1 = x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2
        A2 = 2 * (x3 - x2)
        B2 = 2 * (y3 - y2)
        C2 = x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2
        x = ((C1 * B2) - (C2 * B1)) / ((A1 * B2) - (A2 * B1))
        y = ((A1 * C2) - (A2 * C1)) / ((A1 * B2) - (A2 * B1))
        AO = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        BO = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
        AB = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        angle_AOB = math.acos((AO ** 2 + BO ** 2 - AB ** 2) / 2 / AO / BO)
        print('angle_AOB is {a:.2f} pi, {b:.2f} degrees'.format(a=angle_AOB / math.pi,
                                                                b=angle_AOB * 180 / math.pi))
        clipboard = QApplication.clipboard()
        clipboard.setText('{a:.2f}'.format(a=angle_AOB * 180 / math.pi))
        self.O_mark.set_visible(True)
        self.O_mark.set_xdata(x)
        self.O_mark.set_ydata(y)
        self.O_sign.set_x(x)
        self.O_sign.set_y(y)
        self.O_sign.set_visible(True)
        self.AO_line.set_xdata([x1, x])
        self.AO_line.set_ydata([y1, y])
        self.BO_line.set_xdata([x2, x])
        self.BO_line.set_ydata([y2, y])
        self._imag_show.canvas.draw()

    def _set_layout(self):
        _layout1 = QW.QHBoxLayout()
        _layout1.addWidget(self._imag_show)
        _layout1.addWidget(self._exif_table)
        _layout = QW.QVBoxLayout()
        _layout.addLayout(_layout1)
        _layout.addWidget(self._read_file)
        self.cenWidget.setLayout(_layout)

    def _set_connect(self):
        self._read_file.pathChanged.connect(self.imshow)
        self._imag_show.figure.canvas.mpl_connect('button_press_event', self.click_callback)

    def click_callback(self, event):
        print('clicked on ({x:.0f}, {y:.0f})'.format(x=event.xdata, y=event.ydata))
        if event.button != 1:  # left click is need.
            return None
        if event.key == '1':
            self.set_A_mark(event.xdata, event.ydata)
        elif event.key == '2':
            self.set_B_mark(event.xdata, event.ydata)
        elif event.key == '3':
            self.set_C_mark(event.xdata, event.ydata)
        else:
            return None
        self.set_O_mark()

    def imshow(self):
        print('show_image')
        file_path = self._read_file.path
        im = cv2.imread(file_path)
        b, g, r = cv2.split(im)
        im = cv2.merge([r, g, b])
        self._imag_show.imshow(im)
        self.init_marks()
        self.hide_marks()
        self._imag_show.set_focus()
        exif_info = self.get_exif(file_path)
        for i, key in enumerate(exif_info.keys()):
            self._exif_table.setItem(i, 0, QW.QTableWidgetItem(key))
            self._exif_table.setItem(i, 1, QW.QTableWidgetItem(exif_info[key]))


if __name__ == '__main__':
    if not QW.QApplication.instance():
        app = QW.QApplication(sys.argv)
    else:
        app = QW.QApplication.instance()
    app.setStyle(QW.QStyleFactory.create("Fusion"))
    window = TheWindow()
    window.show()
    app.exec_()
