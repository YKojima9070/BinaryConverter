import cv2
import os
import glob
import numpy as np
import tkinter
import tkinter.filedialog as tkdialog
from tkinter import messagebox
from PIL import Image, ImageTk


class App():
    def __init__(self, root, root_title):
        self.img_list = []
        self.cur_img_num = 0
        self.color_dict = {}

        try:
            self.img_dir_get()

        except:
            print('FileOpenError')

        self.root = root
        self.root.geometry('1680x1050')
        self.root.title(root_title)

        label_button1 = tkinter.Button(self.root, text="バイナリデータ作成", command=self.data_export)
        label_button1.place(x=1450, y=10, width=210, height=50)

        self.v1 = tkinter.IntVar()
        self.v1.set(0)

        radio_bt0 = tkinter.Radiobutton(self.root, text='_class0', value=0, variable=self.v1)
        radio_bt0.place(x=1450, y=100)
        self.box0 = tkinter.Label(self.root, width=5, bg='#FFFFFF')
        self.box0.place(x=1550, y=100)

        radio_bt1 = tkinter.Radiobutton(self.root, text='_class1', value=1, variable=self.v1)
        radio_bt1.place(x=1450, y=150)
        self.box1 = tkinter.Label(self.root, width=5, bg='#FFFFFF')
        self.box1.place(x=1550, y=150)

        radio_bt2 = tkinter.Radiobutton(self.root, text='_class2', value=2, variable=self.v1)
        radio_bt2.place(x=1450, y=200)
        self.box2 = tkinter.Label(self.root, width=5, bg='#FFFFFF')
        self.box2.place(x=1550, y=200)

        radio_bt3 = tkinter.Radiobutton(self.root, text='_class3', value=3, variable=self.v1)
        radio_bt3.place(x=1450, y=250)
        self.box3 = tkinter.Label(self.root, width=5, bg='#FFFFFF')
        self.box3.place(x=1550, y=250)

        radio_bt4 = tkinter.Radiobutton(self.root, text='_class4', value=4, variable=self.v1)
        radio_bt4.place(x=1450, y=300)
        self.box4 = tkinter.Label(self.root, width=5, bg='#FFFFFF')
        self.box4.place(x=1550, y=300)

        iname = tkinter.StringVar(value=self.img_list)

        self.listbox = tkinter.Listbox(self.root, listvariable=iname)
        self.listbox.place(width=210, height=350, x=1450, y=380)
        self.root.bind('<<ListboxSelect>>', self.listbox_callback)

        exit_button = tkinter.Button(self.root, text='Exit', command=self.exit_app)
        exit_button.place(x=1450, y=800, width=210, height=50)


        self.img_canvas = tkinter.Canvas(self.root, width=1400, height=1000)
        self.label_canvas = tkinter.Canvas(self.root, width=1400, height=1000)

        self.img_canvas.bind('<Motion>', self.callback)
        self.img_canvas.bind('<Button>', self.callback)
        self.img_canvas.focus_set()

        self.root.bind_all()

        self.img_show()

        self.root.mainloop()

    def callback(self, event):
        if event.x is not None and event.num == 1:
            pixel_value = self.array_img[event.y, event.x]
            hex_value = '#{:02x}{:02x}{:02x}'.format(pixel_value[0], pixel_value[1], pixel_value[2])
            
            _n = self.v1.get()
            
            if _n == 0:
                self.box0.configure(bg=hex_value)
                self.color_dict['_class0'] = self.hextobgr(hex_value)
            
            elif _n == 1:
                self.box1.configure(bg=hex_value)
                self.color_dict['_class1'] = self.hextobgr(hex_value)

            elif _n == 2:
                self.box2.configure(bg=hex_value)
                self.color_dict['_class2'] = self.hextobgr(hex_value)

            elif _n == 3:
                self.box3.configure(bg=hex_value)
                self.color_dict['_class3'] = self.hextobgr(hex_value)

            elif _n == 4:
                self.box4.configure(bg=hex_value)
                self.color_dict['_class4'] = self.hextobgr(hex_value)

        if event.keysym == 'Right':
            self.cur_img_num += 1
            self.img_show()

        if event.keysym == 'Left':
            self.cur_img_num -= 1
            self.img_show()

    def listbox_callback(self, event):
        if len(self.listbox.curselection()) == 0:
            return
        else:
            self.cur_img_num= self.listbox.curselection()[0]
            self.img_show()


    def hextobgr(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv //3))


    def img_dir_get(self):
        img_format = [".png", ".jpg", ".jpeg", ".bmp", ".JPG"]
        tar_dir = os.path.dirname(tkdialog.askopenfilename(filetypes=[('all_files', '*.*')], initialdir=os.getcwd()))
        self.img_list = [p for p in glob.glob("{0}/**".format(tar_dir), recursive=True) if os.path.splitext(p)[1] in img_format]


    def img_show(self):
        img = cv2.imread(self.img_list[self.cur_img_num])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        self.array_img = self.scale_box(img)
        self.dst_img = Image.fromarray(self.array_img, 'RGBA')
        self.dst_img = ImageTk.PhotoImage(self.dst_img)
        self.img_canvas.create_image(0, 0, image=self.dst_img, anchor='nw')
        self.img_canvas.place(x=0, y=0)


    def scale_box(self, img):
        img_scale = max(1400 / img.shape[1], 1000 / img.shape[0])
        return cv2.resize(img, dsize=None, fx=img_scale, fy=img_scale)


    def data_export(self):
        tar_dir = tkdialog.askdirectory(initialdir=os.getcwd())

        for i in range(len(self.img_list)):
            for n in range(len(self.color_dict)):
                class_name = '_class{0}'.format(n)

                if not self.color_dict.get(class_name) == None:
                    self.binary_change(self.img_list[i], class_name, self.color_dict[class_name], tar_dir)
                else:
                    None

        if tar_dir:
            messagebox.showinfo('情報', '出力完了しました。')
        else:
            None


    def binary_change(self, img_list, class_name, color_thresh, tar_dir):
        img = np.fromfile(img_list, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

        b = img[:, :, 0]
        g = img[:, :, 1]
        r = img[:, :, 2]

        mask = np.zeros(img.shape, dtype=np.uint8)
        mask[(b > color_thresh[0]-30) & (g > color_thresh[1]-30) & (r > color_thresh[2]-30)] = 255
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        ftitle, fpath = os.path.splitext(os.path.basename(img_list))
        
        save_path = tar_dir + '/' + ftitle + class_name + fpath

        _, n = cv2.imencode('.bmp', mask, [int(cv2.IMWRITE_WEBP_QUALITY), 100])

        with open(save_path, mode='w+b') as f:
            n.tofile(f)


    def exit_app(self):
        self.root.destroy()


app_class = App(tkinter.Tk(), 'BinaryConverter v1.0')
