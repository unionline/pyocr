from tkinter.constants import *
from tkinter import Frame
from tkinter import Menu
from tkinter import Button
from tkinter import Text
from tkinter import Label

from tkinter import filedialog
from tkinter.simpledialog import messagebox
from tkinter.messagebox import askyesno
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk


import os

import core.baidu_ocr as core


class Section(Frame):

    def __init__(self, master=None, text=None):
        Frame.__init__(self, master)
        self.master = master
        self.text = text

    def onPaste(self):
        try:
            text = self.master.clipboard_get()
        except TclError:
            pass
        self.text.insert(END, str(text))

    def onCopy(self):
        self.master.clipboard_clear()
        text = self.text.get(1.0, END)
        self.master.clipboard_append(text)

    def onCut(self):
        self.onCopy()
        try:
            self.text.delete(1.0, END)
        except TclError:
            print('cut fail')


class Application(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.init_menu()
        self.createWidgets()
        self.init_var()
        self.init_popMenu()
        self.init_Func()

    def init_window(self):
        print("init_window")
        self.master.title("通用文字识别V0.1")
        self.master.geometry("400x300+100+100")
        self.master.resizable(width=False, height=False)

        self.pack(side=LEFT, expand=YES, fill=BOTH)

    def init_menu(self):
        print("init_menu")
        # 实例化一个Menu对象,这个在主窗体添加一个菜单
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # 创建File菜单,下面有Save和Exit两个子菜单
        file = Menu(menu)
        file.add_command(label='Open Image', command=self.openImage)
        file.add_command(label='Save As Text', command=self.saveText)
        file.add_command(label='Convert', command=self.startConvert)
        file.add_separator()
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        # 创建关于菜单
        about = Menu(menu)
        about.add_command(label='Change Log', command=self.change_log)
        about.add_separator()
        about.add_command(label='About Me', command=self.about_me)
        menu.add_cascade(label='About', menu=about)

    def createWidgets(self):
        print("createWidgets")
        self.frame_left = Frame(self)
        self.frame_left.pack(side=LEFT, padx=3, pady=3, expand=YES, fill=BOTH)

        self.text = ScrolledText(self.frame_left, width=5, height=12)
        self.text.config(font=('Arial', 12))
        self.text.delete('1.0', END)
        self.text.pack(side=TOP, padx=3, pady=3, expand=YES, fill=BOTH)

        self.f2 = Frame(self.frame_left)
        self.btnOpen = Button(self.f2, text='打开图片', command=self.openImage)
        button_opt = {'side': LEFT, 'padx': 3,
                      'pady': 3, 'expand': YES, 'fill': BOTH}
        self.btnOpen.pack(**button_opt)

        self.btnConvert = Button(self.f2, text='开始转换',
                                 command=self.startConvert)
        self.btnConvert.pack(**button_opt)

        button_opt = {'side': RIGHT, 'padx': 3,
                      'pady': 3, 'expand': YES, 'fill': BOTH}

        self.btnShowImg = Button(self.f2, text='显示图片', command=self.showImg)
        self.btnShowImg.pack(**button_opt)

        self.btnSave = Button(self.f2, text='保存文本', command=self.saveText)
        self.btnSave.pack(**button_opt)

        button_opt = {'side': BOTTOM, 'padx': 3,
                      'pady': 3, 'expand': YES, 'fill': BOTH}
        self.f2.pack(**button_opt)

        self.spliter = Label(self, text='', width=2,
                             cursor='sb_h_double_arrow')
        self.spliter.pack(side=LEFT, expand=NO, fill=Y)
        self.spliter.bind("<B1-Motion>", self.changeSize)

        self.imgZone = Label(self, relief=GROOVE, border=3)

    def init_var(self):
        print("init_variable")
        self.flagShowImage = False
        # 上次为False，说明当前是True，永远和flagShowImage相反
        self.flagShowImageLast = True
        self.filename = ''

        self.imgWidth = 400
        self.imgHeight = 300
        self.imgDict = {}
        self.imgZoneWidth = 400

        self.imgZongBg = 'E:/work/learn/gitea/project/AIDemo/bae/images/common/default_bg.png'
        self.filename = self.imgZongBg

    def init_Func(self):
        print("init_Func")
        self.showImg()

    def init_popMenu(self):
        print("init_popMenu")
        section = Section(self.master, self.text)
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="复制", command=section.onCopy)
        menu.add_separator()
        menu.add_command(label="粘贴", command=section.onPaste)
        menu.add_separator()
        menu.add_command(label="剪切", command=section.onCut)

        def pop(event):
            menu.post(event.x_root, event.y_root)

        self.text.bind("<Button-3>", pop)

    def saveText(self):
        
        file_text = self.text.get("1.0", "end")
        if file_text == '\n':
            messagebox.showinfo('提示', '文字框区域为空')
            return
        print("正在保存文本...")
        saveText_filename = filedialog.asksaveasfilename(
            title=u'保存文件', filetypes=[("Text Files", ".txt"), ("All Files", ".*")])

        if saveText_filename[-4:] != ".txt":
            saveText_filename = saveText_filename + ".txt"

        if saveText_filename:
            print("保存文本内容：\n", file_text)
            # file_text = self.text.get("1.0", "end")
            try:
                with open(file=saveText_filename, mode='w', encoding='utf-8') as file:
                    file.write(file_text)
                    print("保存文本成功！")
                messagebox.showinfo('提示', '文件保存成功！')
            except Exception as e:
                messagebox.showinfo('提示', '文件保存失败,原因可能是{}'.format(str(e)))
        else:
            messagebox.showinfo('提示', '未选择文本名称或者文本不存在')

    def openImage(self):
        if self.text.get(1.0, END) != '\n':
            question = askyesno("是否保存", "检测到文本框有内容，是否保存该内容？\n友情提醒：不保存将覆盖原有内容")
            if question:
                self.saveText()

        filenameTemp = filedialog.askopenfilename(
            title=u'选择需要识别的图片',
            defaultextension=".png",
            filetypes=[('All Files', '.*'), ('PNG', '.png'), ('JPEG', '.jpg'), ('SVG', '.svg'), ('TIFF', '.tif'), ('GIF', '.gif')])

        def checkValidFormat(filename, *args):
            dot = '.'
            for ele in args:
                if filename.endswith(dot + ele):
                    return True

            return False

        if filenameTemp != '':
            ok = checkValidFormat(filenameTemp, 'png',
                                  'jpg', 'jpeg', 'svg', 'tif', 'tiff', 'gif')
            if not ok:
                messagebox.showinfo('提示', '请选择图片(格式支持png/jpg/svg/tif/gif)')
                return

            if self.filename != filenameTemp:
                self.filename = filenameTemp
                if self.flagShowImageLast:
                    self.flagShowImage = False
                    self.showImg()
                    print('打开图片名称：', self.filename)
                else:
                    # 没展现图像状态
                    self.startConvert()
                    self.flagShowImage = False

            else:
                messagebox.showinfo('提示', '你选择图片和上一张重复！')

            # self.image_title.config(state=NORMAL)
            # self.image_title.delete(1.0, END)
            # # self.image_title.insert('insert', filenameTemp)
            # self.image_title.insert('insert', filenameTemp[filenameTemp.rfind("/") + 1:])
            # self.image_title.config(state=DISABLED)

        

    def startConvert(self):
        
        if self.filename:
            if self.filename == self.imgZongBg:
                messagebox.showinfo('提示', '请先选择要识别文字的图片')
                return
            print("开始识别图片")
            txt = self.getWord()
            self.btnOpen.config({'text': '请稍候,图片处理中'})
            self.btnOpen.config({'state': DISABLED})
            if txt:
                print("图片识别成功！")
                self.text.delete(1.0, END)
                self.text.insert(1.0, txt)
                self.btnShowImg.config({'state': NORMAL})
            else:
                self.text.insert(1.0, '未识别到内容')
            self.btnOpen.config({'text': '打开图片'})
            self.btnOpen.config({'state': NORMAL})
        else:
            messagebox.showinfo('提示', '请先选择要识别文字的图片')

    def loadImage(self):
        print("加载图片...")
        if self.filename:
            image = Image.open(self.filename)
            resizeImg = self.reSize(
                image.size[0], image.size[1], self.imgWidth, self.imgHeight, image)
            return ImageTk.PhotoImage(resizeImg)
        else:
            messagebox.showinfo('提示', '未选择图片')

    def showImg(self):
        if self.imgDict:
            self.btnShowImg.config({'state': NORMAL})

        if self.flagShowImage:
            self.flagShowImageLast = False
        else:
            self.flagShowImageLast = True

        if not self.flagShowImage:
            if not self.filename:
                messagebox.showinfo('提示', '还未选择图片')
                return

            self.image = self.loadImage()
            self.imgZone.config({'image': self.image})

            self.flagShowImage = True
            self.btnShowImg.config({'text': '隐藏图片'})
            self.imgZone.pack(side=LEFT, fill=BOTH)
            self.imgZone.config(width=self.imgZoneWidth)

            # self.master.geometry('800x300+100+100')
            self.master.geometry('800x300')
            self.imgDict[self.filename] = self.image

            self.btnOpen.config({'text': '打开图片'})
            self.btnConvert.config({'state': NORMAL})

            return self.image
        else:
            self.flagShowImage = False
            self.btnShowImg.config({'text': '显示图片'})
            self.imgZone.pack_forget()
            # self.master.geometry('400x300+100+100')
            self.master.geometry('400x300')

            self.btnOpen.config({'text': '打开图片并识别'})
            self.btnConvert.config({'state': DISABLED})

            return None

    def changeSize(self, event):
        self.imgWidth = self.imgZone.winfo_width() - event.x + 5
        if self.imgWidth < 50:
            self.imgWidth = 50

        self.imgZone.config(width=self.imgWidth)
        self.imgZoneWidth = self.imgWidth

        self.image = self.loadImage()
        self.imgZone.config({'image': self.image})

    def reSize(self, w, h, w_box=400, h_box=300, image=None):
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h

        scale = min([f1, f2])

        width = int(w * scale)
        height = int(h * scale)

        return image.resize((width, height), Image.ANTIALIAS)

    def getWord(self):

        ocr = core.BaiduOCR
        ocr.set_img_path(ocr, self.filename)

        print("请稍候,正在图片识别中...")
        retsult = ocr.img2txt_by_type(
            ocr, core.type_index["Type_basicGeneral"])
        print("识别结果：\n", retsult)
        return retsult

    # 菜单栏
    def client_exit(self):
        exit()

    def about_me(self):
        messagebox.showinfo(
            "About Me", "通用文字识别V0.1\n\n简介：基于Baidu-AIP技术开发\n作者：fanbi\n邮箱：unionline@126.com")

    def change_log(self):
        messagebox.showinfo(
            "Change Log", "版本号：V0.1\n日期：2020-04-09\n开发日志：\n1. 通用文字识别\n2. 第一版界面")
