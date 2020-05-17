import cv2
import os
import glob
import numpy as np
import PySimpleGUI as sg


##使い方##
# iPadの画像でマークアップで赤、青でマーキングされた画像を二値化してNAIT v1.2へインポートできる画像を生成します。

class App():
    def __init__(self):
        self.img_list = []
        self.threshold = 175
        #BGR並び
        self.red_thresh = [72, 54, 243]
        self.blue_thresh = [255, 128, 15]

        img_format = [".png", ".jpg", ".jpeg", ".bmp", ".JPG"]
        tar_dir = os.path.dirname(os.path.abspath(sg.popup_get_file('画像読込')))
        self.img_list = [p for p in glob.glob("{0}/**".format(tar_dir), recursive=True) if os.path.splitext(p)[1] in img_format]

        for i in range(len(self.img_list)):

            self.binary_change(self.img_list[i], '_class0', self.red_thresh)

            self.binary_change(self.img_list[i], '_class1', self.blue_thresh)

    def binary_change(self, img_list, class_name, color_thresh):
        img = np.fromfile(img_list, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

        b = img[:, :, 0]
        g = img[:, :, 1]
        r = img[:, :, 2]

        mask = np.zeros(img.shape, dtype=np.uint8)
        mask[(b > color_thresh[0]-30) & (g > color_thresh[1]-30) & (r > color_thresh[2]-30)] = 255
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        ftitle, fpath = os.path.splitext(img_list)
        save_path = ftitle + class_name + fpath

        _, n = cv2.imencode('.bmp', mask, [int(cv2.IMWRITE_WEBP_QUALITY), 100])

        with open(save_path, mode='w+b') as f:
            n.tofile(f)


App()
