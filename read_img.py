#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15:05 2018/7/28

@author:    Liu Jinbao
@mail:      liu.jinbao@outlook.com
@project:   ReadImg
@IDE:       PyCharm
"""
import math
from matplotlib import pyplot as plt
import cv2

im = cv2.imread(r"E:\PHOTO_exp\JPG\DSC_0457.JPG")  # Read image
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(im)

total_num = 3
out_x = []
out_y = []


def click_callback(event):
    global out_x, out_y
    out_x.append(event.xdata)
    out_y.append(event.ydata)
    print('{x} {y}'.format(x=event.xdata, y=event.ydata))
    if len(out_x) == 3:
        # fig.canvas.mpl_disconnect(cid)
        print(circle_center(out_x, out_y))
        out_x = []
        out_y = []


cid = fig.canvas.mpl_connect('button_press_event', click_callback)


def circle_center(a, b):
    x1, x2, x3 = a
    y1, y2, y3 = b
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
    return math.acos((AO ** 2 + BO ** 2 - AB ** 2) / 2 / AO / BO) * 180 / math.pi
