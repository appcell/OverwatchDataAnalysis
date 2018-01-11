# coding: utf-8
import threading
import time
import tkMessageBox
import tkFileDialog as filedialog
from request import json_request
from Tkinter import (Tk,
                     Frame, Message, Button, Entry,
                     X, LEFT, RIGHT)


def log(*args):
    print args


class Top(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Overwatch Replay Analyzer')
        self.root.geometry('500x300+400+200')

        # path
        self.path_frame = Frame(self.root)
        self.path_frame.pack(fill=X)
        # read
        self.read_frame = Frame(self.path_frame)
        self.read_frame.pack(fill=X)
        self.read_msg = Message(self.read_frame, width=100, text='Video path:')
        self.read_msg.pack(side=LEFT)
        self.read_path = Message(self.read_frame, width=400, text='file1')
        self.read_path.pack(side=LEFT)
        self.read_btn = Button(self.read_frame, text="Choose file", command=self.click_read)
        self.read_btn.pack(side=RIGHT)
        # save
        self.save_frame = Frame(self.path_frame)
        self.save_frame.pack(fill=X)
        self.save_msg = Message(self.save_frame, width=100, text='Save to:')
        self.save_msg.pack(side=LEFT)
        self.save_path = Message(self.save_frame, width=400, text='file2')
        self.save_path.pack(side=LEFT)
        self.save_btn = Button(self.save_frame, text="Choose file", command=self.click_save)
        self.save_btn.pack(side=RIGHT)

        # player
        self.player = Frame(self.root)
        self.player.pack(fill=X, expand=1)
        # left
        self.left_frame = Frame(self.player)
        self.left_frame.pack(side=LEFT)
        self.left_team_name = Entry(self.left_frame, bg='pink', fg='black')
        self.left_team_name.insert(0, 'A队')
        self.left_team_name.pack()
        for i in range(1, 7):
            e = Entry(self.left_frame, bg='red', fg='white')
            name = 'Player' + str(i)
            e.insert(0, name)
            e.pack()
        # right
        self.right_frame = Frame(self.player)
        self.right_frame.pack(side=RIGHT)
        self.right_team_name = Entry(self.right_frame, bg='lightBlue', fg='black')
        self.right_team_name.insert(0, 'B队')
        self.right_team_name.pack()
        for i in range(7, 13):
            e = Entry(self.right_frame, bg='blue', fg='white')
            name = 'Player' + str(i)
            e.insert(0, name)
            e.pack()

        # run
        self.run_btn = Button(self.root, text="Analyze", command=self.run)
        self.run_btn.pack()

        # check for update
        self.t = threading.Thread(target=self.check_update)
        self.t.start()

    def click_btn(self, method):
        filename = filedialog.askopenfilename(initialdir='/')
        if method == 'save':
            self.save_path.config(text=filename)
        else:
            self.read_path.config(text=filename)

    def click_save(self):
        self.click_btn('save')

    def click_read(self):
        self.click_btn('read')

    def check_update(self):
        time.sleep(5)
        version = {'name': 'ORA OWL', 'current_version': '0.1'}
        json_data =  json_request()
        if version['current_version'] == json_data['current_version']:
            pass
        else:
            tkMessageBox.showinfo('版本更新', '有新版本，请更新')

    def show(self):
        self.root.mainloop()

    def run(self):
        tkMessageBox.showinfo('一个微小的弹窗', '保存成功！')


def main():
    top = Top()
    top.show()


if __name__ == '__main__':
    main()
