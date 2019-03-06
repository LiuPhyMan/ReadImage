#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on  10:00 2019/3/6

@author:    Liu Jinbao
@mail:      liu.jinbao@outlook.com
@project:   ReadImage
@IDE:       PyCharm
"""
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

file_path = r"O:\_实验_PHOTOS\2018.07.26\JPG\DSC_0227.JPG"
im_data_rgb = cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
figure = plt.figure()
ax = figure.add_subplot(111)
ax.imshow(im_data_rgb, cmap=plt.get_cmap('gray'))