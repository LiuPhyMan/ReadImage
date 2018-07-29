#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15:05 2018/7/28

@author:    Liu Jinbao
@mail:      liu.jinbao@outlook.com
@project:   ReadImg
@IDE:       PyCharm
"""
from matplotlib import pyplot as plt
import cv2

im = cv2.imread("D:\Desktop\DSC_0759.JPG")  # Read image
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(im)

total_num = 3
out_x = []
out_y = []


def click_callback(event):
    out_x.append(event.xdata)
    out_y.append(event.ydata)
    print('{x} {y}'.format(x=event.xdata, y=event.ydata))
    if len(out_x) == 3:
        fig.canvas.mpl_disconnect(cid)
        print(out_x)
        print(out_y)


cid = fig.canvas.mpl_connect('button_press_event', click_callback)
