#!python3.6.6

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

        ##画面レイアウト##
        self.root = root
        self.root.geometry('1920x1080')
        self.root.title(root_title)
        self.root.configure(bg='#25254f')

        ##tkinter_画像描画部##
        self.img_canvas = tkinter.Canvas(self.root, width=1680, height=1080)
        self.label_canvas = tkinter.Canvas(self.root, width=1400, height=1000)

        self.img_canvas.bind('<Motion>', self.callback)
        self.img_canvas.bind('<Button>', self.callback)

        self.img_canvas.focus_set()
        
        ##tkinter_コントロール部##
        label_button1 = tkinter.Button(self.root, text="バイナリデータ作成", font='Helvetica 14', command=self.data_export, bg='White')
        label_button1.place(x=1700, y=10, width=200, height=50)

        frame = tkinter.Frame(root, width=200, height=450, bg='gray97',  borderwidth=5, relief='groove')
        frame.place(x=1700, y=70)

        self.v1 = tkinter.IntVar()
        self.v1.set(0)

        radio_bt0 = tkinter.Radiobutton(self.root, text='_class0', value=0, variable=self.v1, bg='gray97', fg='Black')
        radio_bt0.place(x=1720, y=100)
        self.box0 = tkinter.Label(self.root, width=4, bg='#FFFFFF', borderwidth=2, relief='raised')
        self.box0.place(x=1820, y=100)

        border1 = tkinter.Frame(root, width=185, height=5, borderwidth=30, relief='groove')
        border1.place(x=1710, y=130)

        radio_bt1 = tkinter.Radiobutton(self.root, text='_class1', value=1, variable=self.v1, bg='gray97', fg='Black')
        radio_bt1.place(x=1720, y=150)
        self.box1 = tkinter.Label(self.root, width=4, bg='#FFFFFF', borderwidth=2, relief='raised')
        self.box1.place(x=1820, y=150)

        border2 = tkinter.Frame(root, width=185, height=5, borderwidth=30, relief='groove')
        border2.place(x=1710, y=180)

        radio_bt2 = tkinter.Radiobutton(self.root, text='_class2', value=2, variable=self.v1, bg='gray97', fg='Black')
        radio_bt2.place(x=1720, y=200)
        self.box2 = tkinter.Label(self.root, width=4, bg='#FFFFFF', borderwidth=2, relief='raised')
        self.box2.place(x=1820, y=200)

        border3 = tkinter.Frame(root, width=185, height=5, borderwidth=30, relief='groove')
        border3.place(x=1710, y=230)

        radio_bt3 = tkinter.Radiobutton(self.root, text='_class3', value=3, variable=self.v1, bg='gray97', fg='Black')
        radio_bt3.place(x=1720, y=250)
        self.box3 = tkinter.Label(self.root, width=4, bg='#FFFFFF', borderwidth=2, relief='raised')
        self.box3.place(x=1820, y=250)

        border4 = tkinter.Frame(root, width=185, height=5, borderwidth=30, relief='groove')
        border4.place(x=1710, y=280)

        radio_bt4 = tkinter.Radiobutton(self.root, text='_class4', value=4, variable=self.v1, bg='gray97', fg='Black')
        radio_bt4.place(x=1720, y=300)
        self.box4 = tkinter.Label(self.root, width=4, bg='#FFFFFF', borderwidth=2, relief='raised')
        self.box4.place(x=1820, y=300)

        border5 = tkinter.Frame(root, width=185, height=5, borderwidth=30, relief='groove')
        border5.place(x=1710, y=350)

        self.lmode = tkinter.BooleanVar()
        lmode_button = tkinter.Checkbutton(root, text='ライブビューモード', variable=self.lmode, command=self.img_show, bg='Black')
        lmode_button.place(x=1720, y=380)

        border6 = tkinter.Frame(root, width=185, height=5, borderwidth=30, relief='groove')
        border6.place(x=1710, y=430)

        self.s_val = tkinter.DoubleVar()
        self.s_val.trace('w', self.s_val_callback)

        scale = tkinter.Scale(root, variable=self.s_val, orient='horizontal', to=100, length=160)
        scale.place(x=1720, y=450)

        exit_button = tkinter.Button(self.root, text='Exit', font='Helvetica 20', command=self.exit_app, bg='White')
        exit_button.place(x=1700, y=950, width=200, height=50)


        ##画像リスト取得＞無しなら終了##
        read_file = self.img_dir_get()

        if self.img_list:
            self.cur_img_num = self.img_list.index(read_file)
            
            ##リストボックス表示##
            iname = tkinter.StringVar(value=self.img_list)
            self.listbox = tkinter.Listbox(self.root, listvariable=iname)
            self.listbox.place(width=200, height=400, x=1700, y=530)
            self.root.bind('<<ListboxSelect>>', self.listbox_callback)

            self.img_read()
            self.img_show()
            
            ##メインループ開始##
            self.root.mainloop()

        else:
            messagebox.showerror('画像読み込みエラー', '起動時に画像選択して下さい。')
            self.exit_app()


    ##マウス、キーボードコールバック##
    def callback(self, event):
        if event.x is not None and event.num == 1:
            pixel_value = self.org_img[event.y, event.x]
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


    ##リストボックスコールバック##
    def listbox_callback(self, event):
        if not len(self.listbox.curselection()) == 0:
            self.cur_img_num = self.listbox.curselection()[0]
            self.img_read()
            self.img_show()
        
        else:
            messagebox.showerror('情報', '画像が見つかりません。')

    ##スライドバーコールバック##
    def s_val_callback(self, *args):
        self.img_show()


    ##16進BGR変換##
    def hextobgr(self, value):
        value = value.lstrip('#')
        value = '{0}{1}{2}'.format(value[4:6], value[2:4], value[0:2])
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv //3))


    ##ディレクトリ取得##
    def img_dir_get(self):
        img_format = [".png", ".jpg", ".jpeg", ".bmp", ".JPG"]
        read_file = tkdialog.askopenfilename(filetypes=[('all_files', '*.*')], initialdir=os.getcwd())
        tar_dir = os.path.dirname(read_file)
        self.img_list = [p for p in glob.glob(r"{0}/*".format(tar_dir), recursive=False) if os.path.splitext(p)[1] in img_format]
        
        return read_file


    ##画像読み込み##
    def img_read(self):
        img = np.fromfile(self.img_list[self.cur_img_num], dtype=np.uint8)
        self.read_img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)


    ##画像表示##
    def img_show(self):

        if self.read_img is not None:
            _s = self.lmode.get()

            if not _s:
                img = cv2.cvtColor(self.read_img, cv2.COLOR_BGR2RGBA)
                self.org_img = self.scale_box(img)
                dst_img = Image.fromarray(self.org_img, 'RGBA')

            else:
                _n = self.v1.get()

                class_dict = {0:'_class0', 1:'_class1', 2:'_class2', 3:'_class3', 4:'_class4'}
                _, img = self.binary_change(self.read_img, self.color_dict[class_dict[_n]])
                img = self.scale_box(img)
                dst_img = Image.fromarray(img, 'L')


            self.dst_img = ImageTk.PhotoImage(dst_img)
            self.img_canvas.create_image(0, 0, image=self.dst_img, anchor='nw')
            self.img_canvas.place(x=0, y=0)
        
        else:
            self.img_list.remove(self.img_list[self.cur_img_num])


    ##画像描画時リサイズ##
    def scale_box(self, img):
        img_scale = max(1400 / img.shape[1], 1000 / img.shape[0])
        return cv2.resize(img, dsize=None, fx=img_scale, fy=img_scale)


    ##データ出力##
    def data_export(self):
        tar_dir = tkdialog.askdirectory(initialdir=os.getcwd())
        error_list = []

        for i in range(len(self.img_list)):
            for n in range(len(self.color_dict)):
                class_name = '_class{0}'.format(n)

                if not self.color_dict.get(class_name) == None:

                    img = np.fromfile(self.img_list[i], dtype=np.uint8)
                    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

                    error_file, mask = self.binary_change(img, self.color_dict[class_name])
                    self.save_img(mask, self.img_list[i], class_name, tar_dir)
                
                    
                    if not error_file == None and not error_file in error_list:
                        error_list.append(error_file)

        messagebox.showinfo('情報', '{0}件 出力完了しました。\n{1}件 未処理画像があります。'.format(i, len(error_list)))


    ##バイナリイメージ変換##
    def binary_change(self, img, color_thresh):
        th_val = self.s_val.get()
        if img is not None:

            b = img[:, :, 0]
            g = img[:, :, 1]
            r = img[:, :, 2]

            mask = np.zeros(img.shape, dtype=np.uint8)

            mask[((b < color_thresh[0] + th_val) & (b > color_thresh[0] - th_val)) & \
                ((g < color_thresh[1] + th_val) & (g > color_thresh[1] - th_val)) & \
                    ((r < color_thresh[2] + th_val) & (r > color_thresh[2] - th_val))] = 255

            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

            return None, mask

        else:
            return img_list, None
        

    ##画像保存##
    def save_img(self, mask, img_list, class_name, tar_dir):        
            ftitle, fpath = os.path.splitext(os.path.basename(img_list))        
            save_path = tar_dir + '/' + ftitle + class_name + fpath
            _, n = cv2.imencode('.png', mask, [int(cv2.IMWRITE_WEBP_QUALITY), 100])
            with open(save_path, mode='w+b') as f:
                n.tofile(f)


    ##アプリ終了##
    def exit_app(self):
        self.root.destroy()

if __name__ == '__main__':
    app_class = App(tkinter.Tk(), 'BinaryConverter v1.0')