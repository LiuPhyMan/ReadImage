import math
import numpy as np
import cv2
from scipy.interpolate import interp2d
from matplotlib import pyplot as plt


def im_read(file_path):
    return cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)


class DrawLine(object):

    def __init__(self, ax0, ax1):
        self.ax0 = ax0
        self.ax1 = ax1
        self.line, = ax0.plot([0, 0], [0, 0],
                              color='yellow',
                              linewidth=1.5, linestyle='-.',
                              alpha=0.5)
        self.in_line, = ax1.plot([], [], '.-')
        self.fwhm_line, = ax1.plot([], [], color='red')
        self.xdata = [None, None]
        self.ydata = [None, None]
        self.set_A_mark()
        self.set_B_mark()
        self.set_fwhm_mark()

    def set_A_mark(self):
        self.A_mark = self.ax0.text(0, 0, 'A')
        self.A_mark.set_size(18)
        self.A_mark.set_color('RED')
        self.A_mark.set_visible(False)
        # self.A_mark.set_visible(True)

    def set_B_mark(self):
        self.B_mark = self.ax0.text(0, 0, 'B')
        self.B_mark.set_size(18)
        self.B_mark.set_color('GREEN')
        self.B_mark.set_visible(False)

    def set_fwhm_mark(self):
        self.fwhm_mark = self.ax1.text(0, 0, 'width = 0')
        self.fwhm_mark.set_size(12)
        self.fwhm_mark.set_color('black')
        self.fwhm_mark.set_visible(False)

    def connect(self):
        self.cid_press = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.line.figure.canvas.mpl_connect('button_release_event',
                                                               self.on_release)
        self.cid_motion = self.line.figure.canvas.mpl_connect('motion_notify_event',
                                                              self.on_motion)

    def on_press(self, event):
        if event.key == 'alt':
            self.xdata[0] = event.xdata
            self.ydata[0] = event.ydata
        self.print_data()

    def on_release(self, event):
        if event.key == 'alt':
            self.xdata[1] = event.xdata
            self.ydata[1] = event.ydata
        self.print_data()
        self.plot_data_on_line()

    def on_motion(self, event):
        if event.button and (event.key == 'alt'):
            self.xdata[1] = event.xdata
            self.ydata[1] = event.ydata
            self.plot_line()
        self.print_data()

    def plot_line(self):
        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        # self.A_mark.set_visible(True)
        # self.B_mark.set_visible(True)
        self.A_mark.set_x(self.xdata[0])
        self.A_mark.set_y(self.ydata[0])
        self.B_mark.set_x(self.xdata[1])
        self.B_mark.set_y(self.ydata[1])
        self.line.figure.canvas.draw()

    def plot_data_on_line(self):
        x_seq = np.linspace(self.xdata[0], self.xdata[1], num=2000)
        y_seq = np.linspace(self.ydata[0], self.ydata[1], num=2000)
        data_on_line = []
        for _x, _y in zip(x_seq, y_seq):
            data_on_line.append(ln_func(_x, _y)[0])
        line_length = math.sqrt((self.xdata[1] - self.xdata[0]) ** 2 +
                                (self.ydata[1] - self.ydata[0]) ** 2)
        data_on_line = np.array(data_on_line)
        self.data_on_line = data_on_line
        self.line_seq = np.linspace(0, line_length, num=2000)
        self.in_line.set_xdata(self.line_seq)
        self.in_line.set_ydata(data_on_line)
        self.ax1.set_xlim(self.line_seq[0], self.line_seq[-1])
        self.ax1.set_ylim(min(data_on_line), max(data_on_line))
        # --------------------------------------------------------------------------------------- #
        fwhm_ratio = 0.5
        fwhm = fwhm_ratio * data_on_line.min() + (1 - fwhm_ratio) * data_on_line.max()
        where_above_fwhm = np.where(data_on_line > fwhm)[0]
        self.data_on_line = data_on_line
        fwhm_left_x = self.line_seq[where_above_fwhm[0]]
        fwhm_left_y = fwhm
        fwhm_right_y = fwhm
        fwhm_right_x = self.line_seq[where_above_fwhm[-1]]
        self.fwhm_line.set_xdata([fwhm_left_x, fwhm_right_x])
        self.fwhm_line.set_ydata([fwhm_left_y, fwhm_right_y])
        self.fwhm_mark.set_x((fwhm_left_x + fwhm_right_x) / 2)
        self.fwhm_mark.set_y(fwhm)
        self.fwhm_mark.set_text('width={:.1f}'.format(fwhm_right_x - fwhm_left_x))
        self.fwhm_mark.set_visible(True)
        np.savetxt("data.txt", np.vstack((self.line_seq, self.data_on_line)).transpose())
        # --------------------------------------------------------------------------------------- #
        self.in_line.figure.canvas.draw()

    def print_data(self):
        pass


# ----------------------------------------------------------------------------------------------- #
image_filename_id = 'DSC_0466.jpg'
im_gray = cv2.imread(r"O:\_EXP_PHOTOS\2018.07.27\JPG\\" + image_filename_id, cv2.IMREAD_GRAYSCALE)
im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_RAINBOW)
fig0 = plt.figure(figsize=(14, 11))
ax0 = fig0.add_subplot(111)
ax0.set_title(image_filename_id)
ax0.imshow(im_color)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ln_func = interp2d(np.arange(im_gray.shape[1]), np.arange(im_gray.shape[0]), im_gray)
ln_draw = DrawLine(ax0, ax1)
ln_draw.connect()
