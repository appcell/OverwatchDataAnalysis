import tkinter.filedialog
from tkinter import (Tk,
                     Frame, Message, Button, Entry,
                     X, LEFT, RIGHT)


def log(*args):
    print(*args)


class Top(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('OW录像分析器')
        self.root.geometry('500x300+400+200')

        # path
        self.path_frame = Frame(self.root)
        self.path_frame.pack(fill=X)
        # read
        self.read_frame = Frame(self.path_frame)
        self.read_frame.pack(fill=X)
        self.read_msg = Message(self.read_frame, width=100, text='读取路径:')
        self.read_msg.pack(side=LEFT)
        self.read_path = Message(self.read_frame, width=400, text='file1')
        self.read_path.pack(side=LEFT)
        self.read_btn = Button(self.read_frame, text="选择文件", command=self.click_read)
        self.read_btn.pack(side=RIGHT)
        # save
        self.save_frame = Frame(self.path_frame)
        self.save_frame.pack(fill=X)
        self.save_msg = Message(self.save_frame, width=100, text='保存路径:')
        self.save_msg.pack(side=LEFT)
        self.save_path = Message(self.save_frame, width=400, text='file2')
        self.save_path.pack(side=LEFT)
        self.save_btn = Button(self.save_frame, text="选择文件", command=self.click_save)
        self.save_btn.pack(side=RIGHT)

        # player
        self.player = Frame(self.root)
        self.player.pack(fill=X, expand=1)
        # left
        self.left_frame = Frame(self.player)
        self.left_frame.pack(side=LEFT)
        for i in range(1, 7):
            e = Entry(self.left_frame, bg='red', fg='white')
            name = '选手' + str(i)
            e.insert(0, name)
            e.pack()
        # right
        self.right_frame = Frame(self.player)
        self.right_frame.pack(side=RIGHT)
        for i in range(7, 13):
            e = Entry(self.right_frame, bg='blue', fg='white')
            name = '选手' + str(i)
            e.insert(0, name)
            e.pack()

        # run
        self.run_btn = Button(self.root, text="开始分析", command=self.run)
        self.run_btn.pack()

    def click_btn(self, method):
        filename = tkinter.filedialog.askopenfilename(initialdir='/')
        if method == 'save':
            self.save_path.config(text=filename)
        else:
            self.read_path.config(text=filename)

    def click_save(self):
        self.click_btn('save')

    def click_read(self):
        self.click_btn('read')

    def show(self):
        self.root.mainloop()

    def run(self):
        pass


def main():
    top = Top()
    top.show()


if __name__ == '__main__':
    main()
